import unittest
from mock import patch

from quickbooks import client


class ClientTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
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

    @patch('quickbooks.client.parse_qs')
    def test_get_authorize_url(self, parse_qs):
        parse_qs.method.return_value = {'oauth_token': '1234', 'oauth_token_secret': '45678'}

        qb_client = client.QuickBooks()
        results = qb_client.get_authorize_url()

        self.assertTrue('https://appcenter.intuit.com/Connect/Begin' in results)
        self.assertTrue('oauth_token' in results)

    @patch('quickbooks.client.QuickBooks.qbService')
    def test_get_access_tokens(self, qbService):
        qb_client = client.QuickBooks()
        qb_client.request_token = "token"
        qb_client.request_token_secret = "secret"
        session = qb_client.get_access_tokens("oauth_verifier")

        qbService.get_auth_session.assert_called_with('token', 'secret', data={'oauth_verifier': 'oauth_verifier'})
        self.assertIsNotNone(session)
