import unittest

from quickbooks import QuickBooks
from quickbooks.objects.purchaseorder import PurchaseOrder


class PurchaseOrderTests(unittest.TestCase):
    def test_unicode(self):
        purchase_order = PurchaseOrder()
        purchase_order.TotalAmt = 1000

        self.assertEquals(str(purchase_order), '1000')

    def test_valid_object_name(self):
        obj = PurchaseOrder()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
