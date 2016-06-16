import unittest

from quickbooks import QuickBooks
from quickbooks.objects.vendorcredit import VendorCredit, ItemBasedExpenseLineDetail, ItemBasedExpenseLine, \
    AccountBasedExpenseLineDetail, AccountBasedExpenseLine


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


class ItemBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEquals(detail.BillableStatus, "")
        self.assertEquals(detail.UnitPrice, 0)
        self.assertEquals(detail.Qty, 0)
        self.assertEquals(detail.TaxInclusiveAmt, 0)


class ItemBasedExpenseLineTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLine()

        self.assertEquals(detail.DetailType, "ItemBasedExpenseLineDetail")
        self.assertEquals(detail.ItemBasedExpenseLineDetail, None)


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = AccountBasedExpenseLineDetail()

        self.assertEquals(detail.BillableStatus, "")
        self.assertEquals(detail.TaxAmount, 0)
        self.assertEquals(detail.TaxInclusiveAmt, 0)


class AccountBasedExpenseLineTests(unittest.TestCase):
    def test_init(self):
        detail = AccountBasedExpenseLine()

        self.assertEquals(detail.DetailType, "AccountBasedExpenseLineDetail")
        self.assertEquals(detail.AccountBasedExpenseLineDetail, None)
