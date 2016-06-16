import unittest

from quickbooks import QuickBooks
from quickbooks.objects.purchase import Purchase, PurchaseLine, AccountBasedExpenseLineDetail, \
    ItemBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = AccountBasedExpenseLineDetail()
        detail.BillableStatus = "Test"

        self.assertEquals(str(detail), "Test")


class PurchaseLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseLine()
        purchase_line.Amount = 100

        self.assertEquals(str(purchase_line), "100")


class PurchaseTests(unittest.TestCase):
    def test_unicode(self):
        purchase = Purchase()
        purchase.TotalAmt = 1000

        self.assertEquals(str(purchase), "1000")

    def test_valid_object_name(self):
        obj = Purchase()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class ItemBasedExpenseLineDetailTest(unittest.TestCase):
    def test_init(self):
        item_detail = ItemBasedExpenseLineDetail()

        self.assertEquals(item_detail.UnitPrice, 0)
        self.assertEquals(item_detail.Qty, 0)
        self.assertEquals(item_detail.BillableStatus, "")
        self.assertEquals(item_detail.TaxInclusiveAmt, 0)
        self.assertEquals(item_detail.ItemRef, None)
        self.assertEquals(item_detail.ClassRef, None)
        self.assertEquals(item_detail.PriceLevelRef, None)
        self.assertEquals(item_detail.TaxCodeRef, None)
        self.assertEquals(item_detail.CustomerRef, None)
        self.assertEquals(item_detail.MarkupInfo, None)