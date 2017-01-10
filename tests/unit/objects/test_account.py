import unittest

from quickbooks import QuickBooks
from quickbooks.objects.account import Account


class AccountTests(unittest.TestCase):
    def test_unicode(self):
        account = Account()
        account.FullyQualifiedName = "test"

        self.assertEquals(str(account), "test")

    def test_to_ref(self):
        account = Account()
        account.FullyQualifiedName = "test"
        account.Id = 12

        ref = account.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Account")
        self.assertEquals(ref.value, 12)

    def test_valid_object_name(self):
        account = Account()
        client = QuickBooks()
        result = client.isvalid_object_name(account.qbo_object_name)

        self.assertTrue(result)