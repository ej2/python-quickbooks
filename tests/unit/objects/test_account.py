import unittest


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
