import unittest

from quickbooks import QuickBooks
from quickbooks.objects.creditmemo import CreditMemo
from quickbooks.objects.detailline import SalesItemLineDetail, \
    DiscountLineDetail, SubtotalLineDetail, DiscountOverride, DescriptionLineDetail


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 10

        self.assertEquals(str(detail), "10")


class CreditMemoTests(unittest.TestCase):
    def test_unicode(self):
        credit_memo = CreditMemo()
        credit_memo.TotalAmt = 1000

        self.assertEquals(str(credit_memo), "1000")

    def test_valid_object_name(self):
        obj = CreditMemo()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class DiscountLineDetailTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEquals(discount_detail.ClassRef, None)
        self.assertEquals(discount_detail.TaxCodeRef, None)
        self.assertEquals(discount_detail.Discount, None)


class SubtotalLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEquals(detail.ItemRef, None)


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountOverride()

        self.assertEquals(discount_detail.PercentBased, False)
        self.assertEquals(discount_detail.DiscountPercent, 0)
        self.assertEquals(discount_detail.DiscountAccountRef, None)
        self.assertEquals(discount_detail.DiscountRef, None)


class DescriptionLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DescriptionLineDetail()

        self.assertEquals(detail.ServiceDate, "")
        self.assertEquals(detail.TaxCodeRef, None)
