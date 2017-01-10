import unittest

from quickbooks import QuickBooks
from quickbooks.objects.vendorcredit import VendorCredit


class VendorCreditTests(unittest.TestCase):
    def test_unicode(self):
        vendor_credit = VendorCredit()
        vendor_credit.TotalAmt = 1000

        self.assertEquals(str(vendor_credit), "1000")

    def test_valid_object_name(self):
        obj = VendorCredit()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

