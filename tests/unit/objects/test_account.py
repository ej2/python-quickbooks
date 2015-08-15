import unittest

from quickbooks.objects.account import Account


class AccountTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        account = Account()
        account.FullyQualifiedName = "test"

        self.assertEquals(account.__unicode__(), "test")
