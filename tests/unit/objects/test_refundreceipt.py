import unittest

from quickbooks.objects.refundreceipt import RefundReceipt, RefundReceiptLine, SalesItemLineDetail


class RefundReceiptTests(unittest.TestCase):
    def test_unicode(self):
        deposit = RefundReceipt()
        deposit.TotalAmt = 100

        self.assertEquals(unicode(deposit), "100")


class RefundReceiptLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = RefundReceiptLine()
        deposit.Amount = 100

        self.assertEquals(unicode(deposit), "100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_init(self):
        sales_item = SalesItemLineDetail()

        self.assertEquals(sales_item.ItemRef, None)
        self.assertEquals(sales_item.TaxCodeRef, None)

