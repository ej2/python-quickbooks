import unittest

from quickbooks.objects.salesreceipt import SalesReceipt


class SalesReceiptTests(unittest.TestCase):
    def test_unicode(self):
        sales_receipt = SalesReceipt()
        sales_receipt.TotalAmt = 100

        self.assertEquals(str(sales_receipt), "100")
