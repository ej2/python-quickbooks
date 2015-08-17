import unittest

from quickbooks.objects.refundreceipt import RefundReceipt, RefundReceiptLine


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