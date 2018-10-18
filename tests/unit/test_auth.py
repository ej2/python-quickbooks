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

    @patch('quickbooks.auth.requests.post')
    def test_get_new_access_tokens_success(self, request_post):

        request_post.return_value = SuccessResponse()

        session_manager = Oauth2SessionManager(
            sandbox=True,
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET',
            access_token='AUTH2_ACCESS_TOKEN',
        )

        session_manager.get_new_access_tokens()

        self.assertEqual(session_manager.x_refresh_token_expires_in, 'expires')
        self.assertEqual(session_manager.access_token, 'access')
        self.assertEqual(session_manager.token_type, 'type')
        self.assertEqual(session_manager.refresh_token, 'refresh')
        self.assertEqual(session_manager.expires_in, 'expires')
        self.assertEqual(session_manager.id_token, 'id')

    @patch('quickbooks.auth.requests.post')
    def test_get_new_access_tokens_failure(self, request_post):
        request_post.return_value = FailureResponse()

        session_manager = Oauth2SessionManager(
            sandbox=True,
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET',
            access_token='AUTH2_ACCESS_TOKEN',
        )

        result = session_manager.get_new_access_tokens()
        self.assertEqual(result, 'error')


class SuccessResponse(object):
    status_code = 200
    text = '{"x_refresh_token_expires_in": "expires", "access_token": "access", "token_type": "type", ' \
           '"refresh_token": "refresh", "expires_in": "expires", "id_token": "id"}'


class FailureResponse(object):
    status_code = 403
    text = 'error'
