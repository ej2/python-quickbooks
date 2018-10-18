import unittest

from quickbooks.exceptions import QuickbooksException

from quickbooks.auth import Oauth1SessionManager, Oauth2SessionManager

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
        )

        self.assertEquals(session_manager.consumer_key, 'key')
        self.assertEquals(session_manager.consumer_secret, 'secret')
        self.assertEquals(session_manager.access_token, 'token')
        self.assertEquals(session_manager.access_token_secret, 'tokensecret')

    def test_start_session(self):
        session_manager = Oauth1SessionManager(
            consumer_key='key',
            consumer_secret='secret',
            access_token='token',
            access_token_secret='tokensecret',
        )

        session = session_manager.start_session()

        self.assertEqual(session.access_token, 'token')
        self.assertEqual(session.access_token_secret, 'tokensecret')
        self.assertEqual(session_manager.started, True)

    def test_start_session_no_consumer_key(self):
        session_manager = Oauth1SessionManager(
            consumer_key='',
            consumer_secret='secret',
            access_token='token',
            access_token_secret='tokensecret',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Consumer Key missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException, session_manager.start_session)

        self.assertEqual(session_manager.started, False)

    def test_start_session_no_consumer_secret(self):
        session_manager = Oauth1SessionManager(
            consumer_key='key',
            consumer_secret='',
            access_token='token',
            access_token_secret='tokensecret',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Consumer Secret missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException, session_manager.start_session)

        self.assertEqual(session_manager.started, False)

    def test_start_session_no_access_token(self):
        session_manager = Oauth1SessionManager(
            consumer_key='key',
            consumer_secret='secret',
            access_token='',
            access_token_secret='tokensecret',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Access Token missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException, session_manager.start_session)

        self.assertEqual(session_manager.started, False)

    def test_start_session_no_token_secret(self):
        session_manager = Oauth1SessionManager(
            consumer_key='key',
            consumer_secret='secret',
            access_token='token',
            access_token_secret='',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Access Token Secret missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException, session_manager.start_session)

        self.assertEqual(session_manager.started, False)


class Oauth2SessionManagerTest(unittest.TestCase):
    def load_session_manager(self, client_id='client_id', client_secret='client_secret', access_token='token', refresh_token='refresh_token'):
        self.session_manager = Oauth2SessionManager(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def setUp(self):
        self.load_session_manager()

    @patch('quickbooks.auth.Oauth2SessionManager.token_request')
    def test_get_tokens_from_code(self, token_request):
        result = self.session_manager.get_access_tokens('code')
        payload = {
            'code': 'code',
            'redirect_uri': self.session_manager.base_url,
            'grant_type': 'authorization_code'
        }
        token_request.assert_called_with(payload, return_result=False)

    @patch('quickbooks.auth.Oauth2SessionManager.token_request')
    def test_refresh_tokens(self, token_request):
        result = self.session_manager.refresh_access_tokens()
        payload = {
            'refresh_token':'refresh_token',                                    
            'grant_type': 'refresh_token'
        }
        token_request.assert_called_with(payload, return_result=False)

    def test_init(self):
        self.assertEqual(self.session_manager.client_id, 'client_id')
        self.assertEqual(self.session_manager.access_token, 'token')
        self.assertEqual(self.session_manager.client_secret, 'client_secret')
        self.assertEqual(self.session_manager.refresh_token, 'refresh_token')

    def test_start_session(self):
        session = self.session_manager.start_session()

        self.assertEqual(session.access_token, 'token')
        self.assertEqual(session.client_secret, 'client_secret')
        self.assertEqual(self.session_manager.started, True)

    def test_start_session_no_client_id(self):
        self.load_session_manager(
            client_id=''
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                self.session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Client Id missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException,
                                  self.session_manager.start_session)

        self.assertEqual(self.session_manager.started, False)

    def test_start_session_no_client_secret(self):
        self.load_session_manager(
            client_secret='',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                self.session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Client Secret missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException,
                                  self.session_manager.start_session)

        self.assertEqual(self.session_manager.started, False)

    def test_start_session_no_access_token(self):
        self.load_session_manager(
            access_token='',
        )

        try:
            with self.assertRaises(QuickbooksException) as error:
                self.session_manager.start_session()

            self.assertEqual(error.exception.message,
                             "Access Token missing. Cannot create session.")
        except:
            self.failUnlessRaises(QuickbooksException,
                                  self.session_manager.start_session)

        self.assertEqual(self.session_manager.started, False)

