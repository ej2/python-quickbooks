import unittest

from quickbooks.objects.purchase import Purchase, PurchaseLine, AccountBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = AccountBasedExpenseLineDetail()
        detail.BillableStatus = "Test"

        self.assertEquals(unicode(detail), "Test")


class PurchaseLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseLine()
        purchase_line.Amount = 100

        self.assertEquals(unicode(purchase_line), "100")


class PurchaseTests(unittest.TestCase):
    def test_unicode(self):
        purchase = Purchase()
        purchase.TotalAmt = 1000

        self.assertEquals(unicode(purchase), "1000")
