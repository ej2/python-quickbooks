import unittest

from quickbooks.objects.vendorcredit import AccountBasedExpenseLineDetail, VendorCreditLine, VendorCredit


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = AccountBasedExpenseLineDetail()
        detail.BillableStatus = "test"

        self.assertEquals(unicode(detail), "test")


class CreditMemoLineTests(unittest.TestCase):
    def test_unicode(self):
        vendor_credit = VendorCreditLine()
        vendor_credit.Amount = 100

        self.assertEquals(unicode(vendor_credit), "100")


class CreditMemoTests(unittest.TestCase):
    def test_unicode(self):
        vendor_credit = VendorCredit()
        vendor_credit.TotalAmt = 1000

        self.assertEquals(unicode(vendor_credit), "1000")
