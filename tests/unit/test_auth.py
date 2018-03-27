import unittest

from quickbooks.exceptions import QuickbooksException

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
