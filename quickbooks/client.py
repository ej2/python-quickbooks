import httplib
import six

from exceptions import QuickbooksException, SevereException

try:
    from rauth import OAuth1Session, OAuth1Service
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")


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
    verbose = False

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

    def __new__(cls, **args):
        if QuickBooks.__instance is None:
            QuickBooks.__instance = object.__new__(cls)

            if 'consumer_key' in args:
                cls.consumer_key = args['consumer_key']

            if 'consumer_secret' in args:
                cls.consumer_secret = args['consumer_secret']

            if 'access_token' in args:
                cls.access_token = args['access_token']

            if 'access_token_secret' in args:
                cls.access_token_secret = args['access_token_secret']

            if 'company_id' in args:
                cls.company_id = args['company_id']

            if 'callback_url' in args:
                cls.callback_url = args['callback_url']

            if 'sandbox' in args:
                cls.sandbox = args['sandbox']

            if 'verbose' in args:
                cls.verbose = True

        return QuickBooks.__instance

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

    def get_authorize_url(self, verify=True):
        """
        Returns the Authorize URL as returned by QB, and specified by OAuth 1.0a.
        :return URI:
        """
        if self.qbService is None:
            self.set_up_service()

        self.request_token, self.request_token_secret = self.qbService.get_request_token(
            params={'oauth_callback': self.callback_url}, verify=verify)

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
        if not request_body:
            request_body = {}

        if self.session is None:
            self.create_session()

        headers = {
            'Content-Type': content_type,
            'Accept': 'application/json'
        }

        req = self.session.request(request_type, url, True, self.company_id, headers=headers, data=request_body)

        try:
            result = req.json()
        except:
            raise QuickbooksException("Error reading json response", 10000, "")

        if req.status_code is not httplib.OK or "Fault" in result:
            self.handle_exceptions(result["Fault"])
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
                code = error["code"]

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
