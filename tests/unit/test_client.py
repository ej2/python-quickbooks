import unittest

from mock import patch

from quickbooks.exceptions import QuickbooksException, SevereException
from quickbooks import client
from quickbooks.objects.salesreceipt import SalesReceipt


class ClientTest(unittest.TestCase):
    def setUp(self):
        pass

    def setUp(self):
        """
        Use a consistent set of defaults.
        """
        client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
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
            consumer_key="consumer_key",
            consumer_secret="consumer_secret",
            access_token="access_token",
            access_token_secret="access_token_secret",
            company_id="company_id",
            callback_url="callback_url",
            verbose=True,
            minorversion=4
        )

        self.assertEquals(self.qb_client.sandbox, False)
        self.assertEquals(self.qb_client.consumer_key, "consumer_key")
        self.assertEquals(self.qb_client.consumer_secret, "consumer_secret")
        self.assertEquals(self.qb_client.access_token, "access_token")
        self.assertEquals(self.qb_client.access_token_secret, "access_token_secret")
        self.assertEquals(self.qb_client.company_id, "company_id")
        self.assertEquals(self.qb_client.callback_url, "callback_url")
        self.assertEquals(self.qb_client.minorversion, 4)

    def test_client_updated(self):
        self.qb_client = client.QuickBooks(
            sandbox=False,
            consumer_key="consumer_key",
            consumer_secret="consumer_secret",
            access_token="access_token",
            access_token_secret="access_token_secret",
            company_id="company_id",
            callback_url="callback_url",
        )

        self.qb_client2 = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url",
        )

        self.assertEquals(self.qb_client.sandbox, True)
        self.assertEquals(self.qb_client.consumer_key, "update_consumer_key")
        self.assertEquals(self.qb_client.consumer_secret, "update_consumer_secret")
        self.assertEquals(self.qb_client.access_token, "update_access_token")
        self.assertEquals(self.qb_client.access_token_secret, "update_access_token_secret")
        self.assertEquals(self.qb_client.company_id, "update_company_id")
        self.assertEquals(self.qb_client.callback_url, "update_callback_url")

        self.assertEquals(self.qb_client2.sandbox, True)
        self.assertEquals(self.qb_client2.consumer_key, "update_consumer_key")
        self.assertEquals(self.qb_client2.consumer_secret, "update_consumer_secret")
        self.assertEquals(self.qb_client2.access_token, "update_access_token")
        self.assertEquals(self.qb_client2.access_token_secret, "update_access_token_secret")
        self.assertEquals(self.qb_client2.company_id, "update_company_id")
        self.assertEquals(self.qb_client2.callback_url, "update_callback_url")

    def test_disable_global(self):
        client.QuickBooks.disable_global()
        self.qb_client = client.QuickBooks()

        self.assertFalse(self.qb_client.sandbox)
        self.assertFalse(self.qb_client.consumer_key)
        self.assertFalse(self.qb_client.consumer_secret)
        self.assertFalse(self.qb_client.access_token)
        self.assertFalse(self.qb_client.access_token_secret)
        self.assertFalse(self.qb_client.company_id)
        self.assertFalse(self.qb_client.callback_url)
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

    def test_get_authorize_url(self):
        qb_client = client.QuickBooks()
        qb_client.set_up_service()

        with patch.object(qb_client.qbService, "get_raw_request_token",
                          return_value=MockResponse()):

            results = qb_client.get_authorize_url()

            self.assertTrue('https://appcenter.intuit.com/Connect/Begin' in results)
            self.assertTrue('oauth_token' in results)
            self.assertEqual(qb_client.request_token, 'tokenvalue')
            self.assertTrue(qb_client.request_token_secret, 'secretvalue')

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_current_user(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        result = qb_client.get_current_user()
        url = "https://appcenter.intuit.com/api/v1/user/current"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.qbService')
    def test_get_access_tokens(self, qbService):
        qb_client = client.QuickBooks()
        qb_client.request_token = "token"
        qb_client.request_token_secret = "secret"
        session = qb_client.get_access_tokens("oauth_verifier")

        qbService.get_auth_session.assert_called_with('token', 'secret', data={'oauth_verifier': 'oauth_verifier'})
        self.assertFalse(session is None)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_disconnect_account(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        result = qb_client.disconnect_account()
        url = "https://appcenter.intuit.com/api/v1/connection/disconnect"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_reconnect_account(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        result = qb_client.reconnect_account()
        url = "https://appcenter.intuit.com/api/v1/connection/reconnect"
        make_req.assert_called_with("GET", url)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_report(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        result = qb_client.get_report("profitandloss", {1: 2})
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/reports/profitandloss"
        make_req.assert_called_with("GET", url, params={1: 2})

    def test_get_instance(self):
        qb_client = client.QuickBooks()

        instance = qb_client.get_instance()
        self.assertEquals(qb_client, instance)

    @patch('quickbooks.client.OAuth1Session')
    def test_create_session(self, auth_Session):
        qb_client = client.QuickBooks()
        session = qb_client.create_session()

        self.assertTrue(auth_Session.called)
        self.assertFalse(session is None)

    def test_create_session_missing_auth_info_exception(self):
        qb_client = client.QuickBooks()
        qb_client.consumer_secret = None

        self.assertRaises(QuickbooksException, qb_client.create_session)

    @patch('quickbooks.client.QuickBooks.make_request')
    def test_get_single_object(self, make_req):
        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"

        result = qb_client.get_single_object("test", 1)
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/test/1/"
        make_req.assert_called_with("GET", url, {})

    @patch('quickbooks.client.QuickBooks.session')
    def test_make_request(self, qb_session):
        qb_session.request.return_value = MockResponse()

        qb_client = client.QuickBooks()
        qb_client.company_id = "1234"
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/test/1/"
        qb_client.make_request("GET", url, request_body=None, content_type='application/json')

        qb_session.request.assert_called_with(
                "GET", url, True, "1234", data={},
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, params={})

    def test_make_request_create_session(self):
        receipt = SalesReceipt()
        receipt.Id = 1
        self.assertRaises(QuickbooksException, receipt.save)

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

    @patch('quickbooks.client.QuickBooks.session')
    def test_download_pdf(self, qb_session):
        qb_client = client.QuickBooks(sandbox=True)
        qb_client.company_id = "1234"
        receipt = SalesReceipt()
        receipt.Id = 1

        receipt.download_pdf()

        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/1234/salesreceipt/1/pdf"
        qb_session.request.assert_called_with(
            "GET", url, True, "1234",
            headers={'Content-Type': 'application/pdf', 'Accept': 'application/pdf, application/json'})

        qb_session.request.return_value = MockPdfResponse()
        response = receipt.download_pdf()

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
