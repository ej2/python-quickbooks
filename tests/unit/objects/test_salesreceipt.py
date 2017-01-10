import unittest

from quickbooks import QuickBooks
from quickbooks.objects.salesreceipt import SalesReceipt


class SalesReceiptTests(unittest.TestCase):
    def test_unicode(self):
        sales_receipt = SalesReceipt()
        sales_receipt.TotalAmt = 100

        self.assertEquals(str(sales_receipt), "100")

    def test_valid_object_name(self):
        obj = SalesReceipt()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
