import unittest

from quickbooks.objects.purchase import Purchase, PurchaseLine, AccountBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = AccountBasedExpenseLineDetail()
        detail.BillableStatus = "Test"

        self.assertEquals(detail.__unicode__(), "Test")


class PurchaseLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseLine()
        purchase_line.Amount = 100

        self.assertEquals(purchase_line.__unicode__(), 100)


class PurchaseTests(unittest.TestCase):
    def test_unicode(self):
        purchase = Purchase()
        purchase.TotalAmt = 1000

        self.assertEquals(purchase.__unicode__(), 1000)
