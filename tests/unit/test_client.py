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

    def test_create_session(self):
        pass

        # qb_client = client.QuickBooks(
        #     sandbox=True,
        #     consumer_key="consumer_key",
        #     consumer_secret="consumer_secret",
        #     access_token="access_token",
        #     access_token_secret="access_token_secret",
        #     company_id="company_id"
        # )
        #
        # session = qb_client.create_session()

    def test_get_authorize_url(self):
        pass

        # qb_client = client.QuickBooks(
        #     sandbox=False,
        #     consumer_key="consumer_key",
        #     consumer_secret="consumer_secret",
        #     access_token="access_token",
        #     access_token_secret="access_token_secret",
        #     company_id="company_id",
        #     callback_url="callback_url",
        #     verbose=True
        # )
        #
        # qb_client.get_authorize_url

