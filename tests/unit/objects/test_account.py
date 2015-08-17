import unittest

from quickbooks.objects.account import Account


class AccountTests(unittest.TestCase):
    def test_unicode(self):
        account = Account()
        account.FullyQualifiedName = "test"

        self.assertEquals(unicode(account), "test")
