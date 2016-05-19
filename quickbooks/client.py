try:  # Python 3
    import http.client as httplib
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    import httplib
    from urlparse import parse_qsl

from .exceptions import QuickbooksException, SevereException, AuthorizationException

try:
    from rauth import OAuth1Session, OAuth1Service
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")
    raise


class QuickBooks(object):
    """A wrapper class around Python's Rauth module for Quickbooks the API"""

    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''
    company_id = 0
    callback_url = ''
    session = None
    sandbox = False
    minorversion = None

    qbService = None

    sandbox_api_url_v3 = "https://sandbox-quickbooks.api.intuit.com/v3"
    api_url_v3 = "https://quickbooks.api.intuit.com/v3"

    request_token_url = "https://oauth.intuit.com/oauth/v1/get_request_token"
    access_token_url = "https://oauth.intuit.com/oauth/v1/get_access_token"

    authorize_url = "https://appcenter.intuit.com/Connect/Begin"

    request_token = ''
    request_token_secret = ''

    _BUSINESS_OBJECTS = [
        "Account", "Attachable", "Bill", "BillPayment",
        "Class", "CompanyInfo", "CreditMemo", "Customer",
        "Department", "Employee", "Estimate", "Invoice",
        "Item", "JournalEntry", "Payment", "PaymentMethod",
        "Preferences", "Purchase", "PurchaseOrder",
        "SalesReceipt", "TaxCode", "TaxRate", "Term",
        "TimeActivity", "Vendor", "VendorCredit"
    ]

    __instance = None
    __use_global = False

    def __new__(cls, **kwargs):
        """
        If global is disabled, don't set global client instance.
        """
        if QuickBooks.__use_global:
            if QuickBooks.__instance is None:
                QuickBooks.__instance = object.__new__(cls)
            instance = QuickBooks.__instance
        else:
            instance = object.__new__(cls)

        if 'consumer_key' in kwargs:
            instance.consumer_key = kwargs['consumer_key']

        if 'consumer_secret' in kwargs:
            instance.consumer_secret = kwargs['consumer_secret']

        if 'access_token' in kwargs:
            instance.access_token = kwargs['access_token']

        if 'access_token_secret' in kwargs:
            instance.access_token_secret = kwargs['access_token_secret']

        if 'company_id' in kwargs:
            instance.company_id = kwargs['company_id']

        if 'callback_url' in kwargs:
            instance.callback_url = kwargs['callback_url']

        if 'sandbox' in kwargs:
            instance.sandbox = kwargs['sandbox']

        if 'minorversion' in kwargs:
            instance.minorversion = kwargs['minorversion']

        return instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    @classmethod
    def disable_global(cls):
        """
        Disable use of singleton pattern.
        """
        QuickBooks.__use_global = False
        QuickBooks.__instance = None

    @classmethod
    def enable_global(cls):
        """
        Allow use of singleton pattern.
        """
        QuickBooks.__use_global = True

    def _drop(self):
        QuickBooks.__instance = None

    @property
    def api_url(self):
        if self.sandbox:
            return self.sandbox_api_url_v3
        else:
            return self.api_url_v3

    def create_session(self):
        if self.consumer_secret and self.consumer_key and self.access_token_secret and self.access_token:
            session = OAuth1Session(
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
            )
            self.session = session
        else:
            raise QuickbooksException("Quickbooks authenication fields not set. Cannot create session.")

        return self.session

    def get_authorize_url(self):
        """
        Returns the Authorize URL as returned by QB, and specified by OAuth 1.0a.
        :return URI:
        """
        self.authorize_url = self.authorize_url[:self.authorize_url.find('?')] if '?' in self.authorize_url else self.authorize_url
        if self.qbService is None:
            self.set_up_service()

        response = self.qbService.get_raw_request_token(
           params={'oauth_callback': self.callback_url})

        oauth_resp = dict(parse_qsl(response.text))

        self.request_token = oauth_resp['oauth_token']
        self.request_token_secret = oauth_resp['oauth_token_secret']

        return self.qbService.get_authorize_url(self.request_token)

    def set_up_service(self):
        self.qbService = OAuth1Service(
            name=None,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            base_url=None
        )

    def get_access_tokens(self, oauth_verifier):
        """
        Wrapper around get_auth_session, returns session, and sets access_token and
        access_token_secret on the QB Object.
        :param oauth_verifier: the oauth_verifier as specified by OAuth 1.0a
        """
        session = self.qbService.get_auth_session(
            self.request_token,
            self.request_token_secret,
            data={'oauth_verifier': oauth_verifier})

        self.access_token = session.access_token
        self.access_token_secret = session.access_token_secret

        return session

    def make_request(self, request_type, url, request_body=None, content_type='application/json'):
        params = {}

        if self.minorversion:
            params['minorversion'] = self.minorversion

        if not request_body:
            request_body = {}

        if self.session is None:
            self.create_session()

        headers = {
            'Content-Type': content_type,
            'Accept': 'application/json'
        }

        req = self.session.request(request_type, url, True, self.company_id, headers=headers, params=params, data=request_body)
        if req.status_code == httplib.UNAUTHORIZED:
            raise AuthorizationException("Application authentication failed", detail=req.text)

        try:
            result = req.json()
        except:
            raise QuickbooksException("Error reading json response: {0}".format(req.text), 10000)

        if "Fault" in result:
            self.handle_exceptions(result["Fault"])
        elif not req.status_code == httplib.OK:
            raise QuickbooksException("Error returned with status code '{0}': {1}".format(
                req.status_code, req.text), 10000)
        else:
            return result

    def get_single_object(self, qbbo, pk):
        url = self.api_url + "/company/{0}/{1}/{2}/".format(self.company_id, qbbo.lower(), pk)
        result = self.make_request("GET", url, {})

        return result

    def handle_exceptions(self, results):
        # Needs to handle multiple errors
        for error in results["Error"]:

            message = error["Message"]

            detail = ""
            if "Detail" in error:
                detail = error["Detail"]

            code = ""
            if "code" in error:
                code = int(error["code"])

            if code >= 10000:
                raise SevereException(message, code, detail)
            else:
                raise QuickbooksException(message, code, detail)

    def create_object(self, qbbo, request_body):
        self.isvalid_object_name(qbbo)

        url = self.api_url + "/company/{0}/{1}".format(self.company_id, qbbo.lower())
        results = self.make_request("POST", url, request_body)

        return results

    def query(self, select):
        url = self.api_url + "/company/{0}/query".format(self.company_id)
        result = self.make_request("POST", url, select, content_type='application/text')

        return result

    def isvalid_object_name(self, object_name):
        if object_name not in self._BUSINESS_OBJECTS:
            raise Exception("{0} is not a valid QBO Business Object.".format(object_name))

        return True

    def update_object(self, qbbo, request_body):
        url = self.api_url + "/company/{0}/{1}".format(self.company_id, qbbo.lower())
        result = self.make_request("POST", url, request_body)

        return result

    def batch_operation(self, request_body):
        url = self.api_url + "/company/{0}/batch".format(self.company_id)
        results = self.make_request("POST", url, request_body)

        return results

    def download_pdf(self, qbbo, item_id):
        url = self.api_url + "/company/{0}/{1}/{2}/pdf".format(self.company_id, qbbo.lower(), item_id)

        if self.session is None:
            self.create_session()

        headers = {
            'Content-Type': 'application/pdf',
            'Accept': 'application/pdf, application/json',
        }

        response = self.session.request("GET", url, True, self.company_id, headers=headers)

        if response.status_code is not httplib.OK:
            try:
                json = response.json()
            except:
                raise QuickbooksException("Error reading json response: {0}".format(response.text), 10000)
            self.handle_exceptions(json["Fault"])
        else:
            return response.content
