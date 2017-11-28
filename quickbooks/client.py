try:  # Python 3
    import http.client as httplib
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    import httplib
    from urlparse import parse_qsl

import textwrap
import json

from .exceptions import QuickbooksException, SevereException, AuthorizationException
import base64

try:
    from rauth import OAuth1Session, OAuth1Service
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")
    raise


class QuickBooks(object):
    company_id = 0
    session = None
    session_manager = None
    sandbox = False
    minorversion = None

    sandbox_api_url_v3 = "https://sandbox-quickbooks.api.intuit.com/v3"
    api_url_v3 = "https://quickbooks.api.intuit.com/v3"

    current_user_url = "https://appcenter.intuit.com/api/v1/user/current"
    disconnect_url = "https://appcenter.intuit.com/api/v1/connection/disconnect"
    reconnect_url = "https://appcenter.intuit.com/api/v1/connection/reconnect"

    _BUSINESS_OBJECTS = [
        "Account", "Attachable", "Bill", "BillPayment",
        "Class", "CreditMemo", "Customer",
        "Department", "Deposit", "Employee", "Estimate", "Invoice",
        "Item", "JournalEntry", "Payment", "PaymentMethod",
        "Purchase", "PurchaseOrder", "RefundReceipt",
        "SalesReceipt", "TaxCode", "TaxService/Taxcode", "TaxRate", "Term",
        "TimeActivity", "Transfer", "Vendor", "VendorCredit"
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

        if 'company_id' in kwargs:
            instance.company_id = kwargs['company_id']

        if 'sandbox' in kwargs:
            instance.sandbox = kwargs['sandbox']

        if 'minorversion' in kwargs:
            instance.minorversion = kwargs['minorversion']

        if 'session_manager' in kwargs:
            instance.session_manager = kwargs['session_manager']

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

    def get_current_user(self):
        """Get data from the current user endpoint"""
        url = self.current_user_url
        result = self.make_request("GET", url)
        return result

    def get_report(self, report_type, qs=None):
        """Get data from the report endpoint"""
        if qs is None:
            qs = {}

        url = self.api_url + "/company/{0}/reports/{1}".format(self.company_id, report_type)
        result = self.make_request("GET", url, params=qs)
        return result

    # TODO: is disconnect url the same for OAuth 1 and OAuth 2?
    def disconnect_account(self):
        """
        Disconnect current account from the application
        :return:
        """
        url = self.disconnect_url
        result = self.make_request("GET", url)
        return result

    def change_data_capture(self, entity_string, changed_since):
        url = self.api_url + "/company/{0}/cdc".format(self.company_id)

        params = {"entities": entity_string, "changedSince": changed_since}

        result = self.make_request("GET", url, params=params)
        return result

    # TODO: is reconnect url the same for OAuth 1 and OAuth 2?
    def reconnect_account(self):
        """
        Reconnect current account by refreshing OAuth access tokens
        :return:
        """
        url = self.reconnect_url
        result = self.make_request("GET", url)
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

    def process_request(self, request_type, url, headers="", params="", data=""):
        if self.session_manager is None:
            raise QuickbooksException('No session manager')

        if self.session_manager.oauth_version == 2.0:
            headers.update({'Authorization': 'Bearer ' + self.session_manager.access_token})
            return self.session_manager.get_session().request(
                request_type, url, headers=headers, params=params, data=data)

        else:
            return self.session_manager.get_session().request(
                request_type, url, True, self.company_id,
                headers=headers, params=params, data=data)

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

    def create_object(self, qbbo, request_body, _file_path=None):
        self.isvalid_object_name(qbbo)

        url = self.api_url + "/company/{0}/{1}".format(self.company_id, qbbo.lower())
        results = self.make_request("POST", url, request_body, file_path=_file_path)

        return results

    def query(self, select):
        url = self.api_url + "/company/{0}/query".format(self.company_id)
        result = self.make_request("POST", url, select, content_type='application/text')

        return result

    def isvalid_object_name(self, object_name):
        if object_name not in self._BUSINESS_OBJECTS:
            raise Exception("{0} is not a valid QBO Business Object.".format(object_name))

        return True

    def update_object(self, qbbo, request_body, _file_path=None):
        url = self.api_url + "/company/{0}/{1}".format(self.company_id, qbbo.lower())
        result = self.make_request("POST", url, request_body, file_path=_file_path)

        return result

    def delete_object(self, qbbo, request_body, _file_path=None):
        url = self.api_url + "/company/{0}/{1}".format(self.company_id, qbbo.lower())
        result = self.make_request("POST", url, request_body, params={'operation': 'delete'}, file_path=_file_path)

        return result

    def batch_operation(self, request_body):
        url = self.api_url + "/company/{0}/batch".format(self.company_id)
        results = self.make_request("POST", url, request_body)

        return results

    def misc_operation(self, end_point, request_body):
        url = self.api_url + "/company/{0}/{1}".format(self.company_id, end_point)
        results = self.make_request("POST", url, request_body)

        return results

    def download_pdf(self, qbbo, item_id):
        if self.session_manager is None:
            raise QuickbooksException('No session manager')

        url = self.api_url + "/company/{0}/{1}/{2}/pdf".format(
            self.company_id, qbbo.lower(), item_id)

        headers = {
            'Content-Type': 'application/pdf',
            'Accept': 'application/pdf, application/json',
            'User-Agent': 'python-quickbooks V3 library'
        }

        response = self.process_request("GET", url, headers=headers)

        if response.status_code != httplib.OK:
            try:
                result = response.json()
            except:
                raise QuickbooksException("Error reading json response: {0}".format(response.text), 10000)

            self.handle_exceptions(result["Fault"])
        else:
            return response.content
