import unittest
from mock import patch

from quickbooks.exceptions import QuickbooksException


class QuickbooksExceptionTests(unittest.TestCase):
    def test_init(self):
        exception = QuickbooksException("message", 100, "detail")

        self.assertEquals(exception.message, "message")
        self.assertEquals(exception.error_code, 100)
        self.assertEquals(exception.detail, "detail")
