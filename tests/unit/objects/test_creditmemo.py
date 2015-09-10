import unittest

from quickbooks.objects.creditmemo import SalesItemLineDetail, CreditMemoLine, CreditMemo, DiscountLineDetail


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 10

        self.assertEquals(unicode(detail), "10")


class CreditMemoLineTests(unittest.TestCase):
    def test_unicode(self):
        memo_line = CreditMemoLine()
        memo_line.LineNum = 1
        memo_line.Description = "Product Description"
        memo_line.Amount = 100

        self.assertEquals(unicode(memo_line), "[1] Product Description 100")


class CreditMemoTests(unittest.TestCase):
    def test_unicode(self):
        credit_memo = CreditMemo()
        credit_memo.TotalAmt = 1000

        self.assertEquals(unicode(credit_memo), "1000")


class DiscountLineDetailTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEquals(discount_detail.ClassRef, None)
        self.assertEquals(discount_detail.TaxCodeRef, None)
        self.assertEquals(discount_detail.Discount, None)
