import unittest

from quickbooks import QuickBooks
from quickbooks.objects.purchase import Purchase


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