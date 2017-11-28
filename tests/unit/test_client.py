import unittest

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from quickbooks.auth import Oauth1SessionManager
from quickbooks.exceptions import QuickbooksException, SevereException
from quickbooks import client
from quickbooks.objects.salesreceipt import SalesReceipt


class ClientTest(unittest.TestCase):
    def setUp(self):
        """
        Use a consistent set of defaults.
        """

        client.QuickBooks(
            session_manager=MockSessionManager(),
            sandbox=True,
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    def tearDown(self):
        client.QuickBooks.enable_global()
        self.qb_client = client.QuickBooks()
        self.qb_client._drop()

    def test_client_new(self):
        self.qb_client = client.QuickBooks(
            sandbox=False,
            company_id="company_id",
            verbose=True,
            minorversion=4
        )

        self.assertEquals(self.qb_client.sandbox, False)
        self.assertEquals(self.qb_client.company_id, "company_id")
        self.assertEquals(self.qb_client.minorversion, 4)

    def test_client_updated(self):
        self.qb_client = client.QuickBooks(
            sandbox=False,
            company_id="company_id",
        )

        self.qb_client2 = client.QuickBooks(
            sandbox=True,
            company_id="update_company_id",
        )

        self.assertEquals(self.qb_client.sandbox, True)
        self.assertEquals(self.qb_client.company_id, "update_company_id")

        self.assertEquals(self.qb_client2.sandbox, True)
        self.assertEquals(self.qb_client2.company_id, "update_company_id")

    def test_disable_global(self):
        client.QuickBooks.disable_global()
        self.qb_client = client.QuickBooks()

        self.assertFalse(self.qb_client.sandbox)
        self.assertFalse(self.qb_client.company_id)
        self.assertFalse(self.qb_client.minorversion)

    def test_api_url(self):
        qb_client = client.QuickBooks(sandbox=False)
        api_url = qb_client.api_url

        self.assertFalse("sandbox" in api_url)

    def test_api_url_sandbox(self):
        qb_client = client.QuickBooks(sandbox=True)
        api_url = qb_client.api_url

        self.assertTrue("sandbox" in api_url)

    def test_isvalid_object_name_valid(self):
        qb_client = client.QuickBooks()
        result = qb_client.isvalid_object_name("Customer")

        self.assertEquals(result, True)

    def test_isvalid_object_name_invalid(self):
        qb_client = client.QuickBooks()

        self.assertRaises(Exception, qb_client.isvalid_object_name, "invalid")

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_batch_operation(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.batch_operation("request_body")

        self.assertTrue(make_req.called)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_misc_operation(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.misc_operation("end_point", "request_body")

        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/update_company_id/end_point"
        make_req.assert_called_with("POST", url, "request_body")

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_create_object(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.create_object("Customer", "request_body")

        self.assertTrue(make_req.called)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_query(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.query("select")

        self.assertTrue(make_req.called)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_update_object(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.update_object("Customer", "request_body")

        self.assertTrue(make_req.called)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_current_user(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        qb_client.get_current_user()
        url = "https://appcenter.intuit.com/api/v1/user/current"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_disconnect_account(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        qb_client.disconnect_account()
        url = "https://appcenter.intuit.com/api/v1/connection/disconnect"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_reconnect_account(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        qb_client.reconnect_account()
        url = "https://appcenter.intuit.com/api/v1/connection/reconnect"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_report(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        qb_client.get_report("profitandloss", {1: 2})
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/reports/profitandloss"
        make_req.assert_called_with("GET", url, params={1: 2})

    def test_get_instance(self):
        qb_client = client.QuickBooks()

        instance = qb_client.get_instance()
        self.assertEquals(qb_client, instance)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_single_object(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        qb_client.get_single_object("test", 1)
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/test/1/"
        make_req.assert_called_with("GET", url, {})

    @patch('quickbooks.client.QuickBooks.process_request')
    def test_make_request(self, process_request):
        process_request.return_value = MockResponse()

        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/test/1/"
        qb_client.make_request("GET", url, request_body=None, content_type='application/json')

        process_request.assert_called_with(
                "GET", url, data={},
                headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'python-quickbooks V3 library'}, params={})

    def test_handle_exceptions(self):
        qb_client = client.QuickBooks()
        error_data = {
            "Error": [{
                "Message": "message",
                "Detail": "detail",
                "code": "2030",
                "element": "Id"}],
            "type": "ValidationFault"
        }

        self.assertRaises(QuickbooksException, qb_client.handle_exceptions, error_data)

    def test_handle_exceptions_severe(self):
        qb_client = client.QuickBooks()
        error_data = {
            "Error": [{
                "Message": "message",
                "Detail": "detail",
                "code": "10001",
                "element": "Id"}],
            "type": "ValidationFault"
        }

        self.assertRaises(SevereException, qb_client.handle_exceptions, error_data)

    @patch('quickbooks.client.QuickBooks.process_request')
    def test_download_pdf(self, process_request):
        qb_client = client.QuickBooks(sandbox=True)
        qb_client.company_id = "1234"
        receipt = SalesReceipt()
        receipt.Id = 1

        process_request.return_value = MockPdfResponse()

        response = receipt.download_pdf(qb_client)

        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/salesreceipt/1/pdf"
        process_request.assert_called_with(
            "GET", url, headers={'Content-Type': 'application/pdf', 'Accept': 'application/pdf, application/json', 'User-Agent': 'python-quickbooks V3 library'})

        self.assertEqual(response, 'sample pdf content')

    def test_download_nonexistent_pdf(self):
        receipt = SalesReceipt()
        receipt.Id = 666
        self.assertRaises(QuickbooksException, receipt.download_pdf)


class MockResponse(object):
    @property
    def text(self):
        return "oauth_token_secret=secretvalue&oauth_callback_confirmed=true&oauth_token=tokenvalue"

    @property
    def status_code(self):
        try:
            import httplib  # python 2
        except ImportError:
            import http.client as httplib  # python 3
        return httplib.OK

    def json(self):
        return "{}"

    def content(self):
        return ''


class MockPdfResponse(object):
    @property
    def status_code(self):
        try:
            import httplib  # python 2
        except ImportError:
            import http.client as httplib  # python 3
        return httplib.OK

    @property
    def content(self):
        return "sample pdf content"


class MockSessionManager(object):
    def get_session(self):
        return MockSession()


class MockSession(object):
    def request(self, request_type, url, no_idea, company_id, **kwargs):
        return MockResponse()
