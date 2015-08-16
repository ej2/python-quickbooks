import unittest

from quickbooks.objects.payment import PaymentLine, Payment


class PaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        memo_line = PaymentLine()
        memo_line.LineNum = 1
        memo_line.Description = "Product Description"
        memo_line.Amount = 100

        self.assertEquals(memo_line.__unicode__(), "[1] Product Description 100")


class PaymentTests(unittest.TestCase):
    def test_unicode(self):
        credit_memo = Payment()
        credit_memo.TotalAmt = 1000

        self.assertEquals(credit_memo.__unicode__(), 1000)
