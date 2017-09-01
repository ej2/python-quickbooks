import unittest

from quickbooks.auth import Oauth1SessionManager

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


class Oauth1SessionManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        session_manager = Oauth1SessionManager(
            consumer_key='key',
            consumer_secret='secret',
            access_token='token',
            access_token_secret='tokensecret',
            callback_url='http://localhost',
            sandbox=True
        )

        self.assertEquals(session_manager.consumer_key, 'key')
        self.assertEquals(session_manager.consumer_secret, 'secret')
        self.assertEquals(session_manager.access_token, 'token')
        self.assertEquals(session_manager.access_token_secret, 'tokensecret')
        self.assertEquals(session_manager.callback_url, 'http://localhost')
        self.assertEquals(session_manager.sandbox, True)
