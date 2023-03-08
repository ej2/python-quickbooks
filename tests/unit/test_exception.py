import unittest


from quickbooks.exceptions import QuickbooksException, AuthorizationException


class QuickbooksExceptionTests(unittest.TestCase):
    def test_init(self):
        exception = QuickbooksException("message", 100, "detail")

        self.assertEqual(exception.message, "message")
        self.assertEqual(exception.error_code, 100)
        self.assertEqual(exception.detail, "detail")


class AuthorizationExceptionTests(unittest.TestCase):
    def test_unicode(self):
        exception = AuthorizationException("message", detail="detail")

        self.assertEqual(str(exception), "QB Auth Exception 0: message\ndetail")
