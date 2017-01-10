import unittest

from quickbooks import QuickBooks
from quickbooks.objects.refundreceipt import RefundReceipt


class RefundReceiptTests(unittest.TestCase):
    def test_unicode(self):
        deposit = RefundReceipt()
        deposit.TotalAmt = 100

        self.assertEquals(str(deposit), "100")

    def test_valid_object_name(self):
        obj = RefundReceipt()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)