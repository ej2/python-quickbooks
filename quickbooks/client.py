try:  # Python 3
    import http.client as httplib
    from urllib.parse import parse_qsl
    from functools import partial
    to_bytes = lambda value, *args, **kwargs: bytes(value, "utf-8", *args, **kwargs)
except ImportError:  # Python 2
    import httplib
    from urlparse import parse_qsl
    to_bytes = str

import textwrap
import codecs
import json

from . import exceptions
import base64
import hashlib
import hmac

try:
    from rauth import OAuth1Session, OAuth1Service, OAuth2Session
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")
    raise


class Environments(object):
    SANDBOX = 'sandbox'
    PRODUCTION = 'production'


class QuickBooks(object):
    company_id = 0
    session = None
    auth_client = None
    sandbox = False
    minorversion = None
    verifier_token = None

    sandbox_api_url_v3 = "https://sandbox-quickbooks.api.intuit.com/v3"
    api_url_v3 = "https://quickbooks.api.intuit.com/v3"
    current_user_url = "https://appcenter.intuit.com/api/v1/user/current"

    _BUSINESS_OBJECTS = [
        "Account", "Attachable", "Bill", "BillPayment",
        "Class", "CreditMemo", "Customer", "CompanyCurrency",
        "Department", "Deposit", "Employee", "Estimate", "Invoice",
        "Item", "JournalEntry", "Payment", "PaymentMethod",
        "Purchase", "PurchaseOrder", "RefundReceipt",
        "SalesReceipt", "TaxAgency", "TaxCode", "TaxService/Taxcode", "TaxRate", "Term",
        "TimeActivity", "Transfer", "Vendor", "VendorCredit", "CreditCardPayment",
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

        if 'refresh_token' in kwargs:
            instance.refresh_token = kwargs['refresh_token']

        if 'auth_client' in kwargs:
            instance.auth_client = kwargs['auth_client']

            if instance.auth_client.environment == Environments.SANDBOX:
                instance.sandbox = True
            else:
                instance.sandbox = False

            instance._start_session()

        if 'company_id' in kwargs:
            instance.company_id = kwargs['company_id']

        if 'minorversion' in kwargs:
            instance.minorversion = kwargs['minorversion']

        if 'verifier_token' in kwargs:
            instance.verifier_token = kwargs.get('verifier_token')

        return instance

    def _start_session(self):
        if self.auth_client.access_token is None:
            self.auth_client.refresh(refresh_token=self.refresh_token)

        self.session = OAuth2Session(
            client_id=self.auth_client.client_id,
            client_secret=self.auth_client.client_secret,
            access_token=self.auth_client.access_token,
        )

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

    def validate_webhook_signature(self, request_body, signature, verifier_token=None):
        hmac_verifier_token_hash = hmac.new(
            to_bytes(verifier_token or self.verifier_token),
            request_body.encode('utf-8'),
            hashlib.sha256
        ).digest()
        decoded_hex_signature = base64.b64decode(signature)
        return hmac_verifier_token_hash == decoded_hex_signature

    def get_current_user(self):
        """Get data from the current user endpoint"""
        url = self.current_user_url
        result = self.get(url)
        return result

    def get_report(self, report_type, qs=None):
        """Get data from the report endpoint"""
        if qs is None:
            qs = {}

        url = self.api_url + "/company/{0}/reports/{1}".format(self.company_id, report_type)
        result = self.get(url, params=qs)
        return result

    def change_data_capture(self, entity_string, changed_since):
        url = "{0}/company/{1}/cdc".format(self.api_url, self.company_id)

        params = {"entities": entity_string, "changedSince": changed_since}

        result = self.get(url, params=params)
        return result

    def make_request(self, request_type, url, request_body=None, content_type='application/json',
                     params=None, file_path=None):
        if not params:
            params = {}

        if self.minorversion:
            params['minorversion'] = self.minorversion

        if not request_body:
            request_body = {}

        headers = {
            'Content-Type': content_type,
            'Accept': 'application/json',
            'User-Agent': 'python-quickbooks V3 library'
        }

        if file_path:
            attachment = open(file_path, 'rb')
            url = url.replace('attachable', 'upload')
            boundary = '-------------PythonMultipartPost'
            headers.update({
                'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                'Accept-Encoding': 'gzip;q=1.0,deflate;q=0.6,identity;q=0.3',
                'User-Agent': 'python-quickbooks V3 library',
                'Accept': 'application/json',
                'Connection': 'close'
            })

            binary_data = str(base64.b64encode(attachment.read()).decode('ascii'))

            content_type = json.loads(request_body)['ContentType']

            request_body = textwrap.dedent(
                """
                --%s
                Content-Disposition: form-data; name="file_metadata_01"
                Content-Type: application/json

                %s

                --%s
                Content-Disposition: form-data; name="file_content_01"
                Content-Type: %s
                Content-Transfer-Encoding: base64

                %s

                --%s--
                """
            ) % (boundary, request_body, boundary, content_type, binary_data, boundary)

            # make sure request_body is not unicode (python 2 case)
            request_body = str(request_body)

        req = self.process_request(request_type, url, headers=headers, params=params, data=request_body)

        if req.status_code == httplib.UNAUTHORIZED:
            raise exceptions.AuthorizationException("Application authentication failed", detail=req.text)

        try:
            result = req.json()
        except:
            raise exceptions.QuickbooksException("Error reading json response: {0}".format(req.text), 10000)

        if "Fault" in result:
            self.handle_exceptions(result["Fault"])
        elif not req.status_code == httplib.OK:
            raise exceptions.QuickbooksException("Error returned with status code '{0}': {1}".format(
                req.status_code, req.text), 10000)
        else:
            return result

    def get(self, *args, **kwargs):
        return self.make_request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.make_request("POST", *args, **kwargs)

    def process_request(self, request_type, url, headers="", params="", data=""):
        if self.session is None:
            raise exceptions.QuickbooksException('No session manager')

        headers.update({'Authorization': 'Bearer ' + self.session.access_token})

        return self.session.request(
            request_type, url, headers=headers, params=params, data=data)

    def get_single_object(self, qbbo, pk):
        url = "{0}/company/{1}/{2}/{3}/".format(self.api_url, self.company_id, qbbo.lower(), pk)
        result = self.get(url, {})

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

            if code > 0 and code <= 499:
                raise exceptions.AuthorizationException(message, code, detail)
            elif code >= 500 and code <= 599:
                raise exceptions.UnsupportedException(message, code, detail)
            elif code >= 600 and code <= 1999:
                if code == 610:
                    raise exceptions.ObjectNotFoundException(message, code, detail)
                raise exceptions.GeneralException(message, code, detail)
            elif code >= 2000 and code <= 4999:
                raise exceptions.ValidationException(message, code, detail)
            elif code >= 10000:
                raise exceptions.SevereException(message, code, detail)
            else:
                raise exceptions.QuickbooksException(message, code, detail)

    def create_object(self, qbbo, request_body, _file_path=None):
        self.isvalid_object_name(qbbo)

        url = "{0}/company/{1}/{2}".format(self.api_url, self.company_id, qbbo.lower())
        results = self.post(url, request_body, file_path=_file_path)

        return results

    def query(self, select):
        url = "{0}/company/{1}/query".format(self.api_url, self.company_id)
        result = self.post(url, select, content_type='application/text')

        return result

    def isvalid_object_name(self, object_name):
        if object_name not in self._BUSINESS_OBJECTS:
            raise Exception("{0} is not a valid QBO Business Object.".format(object_name))

        return True

    def update_object(self, qbbo, request_body, _file_path=None):
        url = "{0}/company/{1}/{2}".format(self.api_url, self.company_id,  qbbo.lower())
        result = self.post(url, request_body, file_path=_file_path)

        return result

    def delete_object(self, qbbo, request_body, _file_path=None):
        url = "{0}/company/{1}/{2}".format(self.api_url, self.company_id, qbbo.lower())
        result = self.post(url, request_body, params={'operation': 'delete'}, file_path=_file_path)

        return result

    def batch_operation(self, request_body):
        url = "{0}/company/{1}/batch".format(self.api_url, self.company_id)
        results = self.post(url, request_body)

        return results

    def misc_operation(self, end_point, request_body, content_type='application/json'):
        url = "{0}/company/{1}/{2}".format(self.api_url, self.company_id, end_point)
        results = self.post(url, request_body, content_type)

        return results

    def download_pdf(self, qbbo, item_id):
        if self.session is None:
            raise exceptions.QuickbooksException('No session')

        url = "{0}/company/{1}/{2}/{3}/pdf".format(
            self.api_url, self.company_id, qbbo.lower(), item_id)

        headers = {
            'Content-Type': 'application/pdf',
            'Accept': 'application/pdf, application/json',
            'User-Agent': 'python-quickbooks V3 library'
        }

        response = self.process_request("GET", url, headers=headers)

        if response.status_code != httplib.OK:

            if response.status_code == httplib.UNAUTHORIZED:
                # Note that auth errors have different result structure which can't be parsed by handle_exceptions()
                raise exceptions.AuthorizationException("Application authentication failed", detail=response.text)

            try:
                result = response.json()
            except:
                raise exceptions.QuickbooksException("Error reading json response: {0}".format(response.text), 10000)

            self.handle_exceptions(result["Fault"])
        else:
            return response.content
