import unittest

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from quickbooks.tools.auth import QuickBooksAuthServer


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.consumer_key = 'update_consumer_key'
        self.consumer_secret = 'update_consumer_secret'
        self.sandbox = True
        self.port = 8080
        self.authorize_url = '{0}?oauth_token=testToken'.format(
            QuickBooksAuthServer.client.authorize_url)

    # def test_build_server(self):
    #     with patch.object(QuickBooksAuthServer.client,
    #                       'get_authorize_url',
    #                       return_value=self.authorize_url):
    #         server = QuickBooksAuthServer.build_server(
    #             self.consumer_key, self.consumer_secret,
    #             self.sandbox, self.port, 2)
    #
    #         self.assertTrue(isinstance(server, QuickBooksAuthServer))
    #         self.assertTrue(isinstance(server.qb_data, dict))
    #         self.assertTrue('oauth_token' in server.qb_data['authorize_url'])
