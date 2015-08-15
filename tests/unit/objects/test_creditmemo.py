import unittest

from quickbooks.objects.creditmemo import SalesItemLineDetail, CreditMemoLine, CreditMemo


class SalesItemLineDetailTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 10

        self.assertEquals(detail.__unicode__(), 10)


class CreditMemoLineTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        memo_line = CreditMemoLine()
        memo_line.LineNum = 1
        memo_line.Description = "Product Description"
        memo_line.Amount = 100

        self.assertEquals(memo_line.__unicode__(), "[1] Product Description 100")


class CreditMemoTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        credit_memo = CreditMemo()
        credit_memo.TotalAmt = 1000

        self.assertEquals(credit_memo.__unicode__(), 1000)
