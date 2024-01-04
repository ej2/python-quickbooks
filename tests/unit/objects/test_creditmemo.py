import unittest

from quickbooks import QuickBooks
from quickbooks.objects.creditmemo import CreditMemo
from quickbooks.objects.detailline import SalesItemLineDetail, \
    DiscountLineDetail, SubtotalLineDetail, DiscountOverride, DescriptionLineDetail


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 10

        self.assertEqual(str(detail), "10")


class CreditMemoTests(unittest.TestCase):
    def test_unicode(self):
        credit_memo = CreditMemo()
        credit_memo.TotalAmt = 1000

        self.assertEqual(str(credit_memo), "1000")

    def test_valid_object_name(self):
        obj = CreditMemo()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        obj = CreditMemo()
        obj.Id = 123

        ref = obj.to_ref()
        self.assertEqual(ref.value, obj.Id)
        self.assertEqual(ref.type, "CreditMemo")


class DiscountLineDetailTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEqual(discount_detail.ClassRef, None)
        self.assertEqual(discount_detail.TaxCodeRef, None)
        self.assertEqual(discount_detail.Discount, None)


class SubtotalLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEqual(detail.ItemRef, None)


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountOverride()

        self.assertEqual(discount_detail.PercentBased, False)
        self.assertEqual(discount_detail.DiscountPercent, 0)
        self.assertEqual(discount_detail.DiscountAccountRef, None)
        self.assertEqual(discount_detail.DiscountRef, None)


class DescriptionLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DescriptionLineDetail()

        self.assertEqual(detail.ServiceDate, "")
        self.assertEqual(detail.TaxCodeRef, None)
