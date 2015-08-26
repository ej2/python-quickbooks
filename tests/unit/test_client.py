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
            verbose=True
        )

        self.assertEquals(self.qb_client.sandbox, False)
        self.assertEquals(self.qb_client.consumer_key, "consumer_key")
        self.assertEquals(self.qb_client.consumer_secret, "consumer_secret")
        self.assertEquals(self.qb_client.access_token, "access_token")
        self.assertEquals(self.qb_client.access_token_secret, "access_token_secret")
        self.assertEquals(self.qb_client.company_id, "company_id")
        self.assertEquals(self.qb_client.callback_url, "callback_url")
        self.assertEquals(self.qb_client.verbose, True)

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

        with self.assertRaises(Exception):
            qb_client.isvalid_object_name("invalid")

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
