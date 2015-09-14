import unittest

from quickbooks.objects.refundreceipt import RefundReceipt


class RefundReceiptTests(unittest.TestCase):
    def test_unicode(self):
        deposit = RefundReceipt()
        deposit.TotalAmt = 100

        self.assertEquals(unicode(deposit), "100")
