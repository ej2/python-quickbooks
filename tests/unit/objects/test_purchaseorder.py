import unittest

from quickbooks.objects.purchaseorder import PurchaseOrderLine, PurchaseOrder, ItemBasedExpenseLineDetail


class PurchaseOrderLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseOrderLine()
        purchase_line.Amount = 100

        self.assertEquals(str(purchase_line), '100')


class PurchaseOrderTests(unittest.TestCase):
    def test_unicode(self):
        purchase_order = PurchaseOrder()
        purchase_order.TotalAmt = 1000

        self.assertEquals(str(purchase_order), '1000')


class ItemBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEquals(detail.UnitPrice, 0)
        self.assertEquals(detail.Qty, 0)
        self.assertEquals(detail.BillableStatus, "")
        self.assertEquals(detail.TaxInclusiveAmt, 0)
        self.assertEquals(detail.PriceLevelRef, None)
        self.assertEquals(detail.CustomerRef, None)
        self.assertEquals(detail.ClassRef, None)
        self.assertEquals(detail.TaxCodeRef, None)
        self.assertEquals(detail.MarkupInfo, None)
