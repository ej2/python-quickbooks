import unittest


from quickbooks.exceptions import QuickbooksException, AuthorizationException


class QuickbooksExceptionTests(unittest.TestCase):
    def test_init(self):
        exception = QuickbooksException("message", 100, "detail")

        self.assertEquals(exception.message, "message")
        self.assertEquals(exception.error_code, 100)
        self.assertEquals(exception.detail, "detail")


class AuthorizationExceptionTests(unittest.TestCase):
    def test_unicode(self):
        exception = AuthorizationException("message", detail="detail")

        self.assertEquals(str(exception), "QB Auth Exception: message \n\ndetail")
