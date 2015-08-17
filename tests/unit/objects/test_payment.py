import unittest

from quickbooks.objects.payment import PaymentLine, Payment


class PaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        payment_line = PaymentLine()
        payment_line.LineNum = 1
        payment_line.Description = "Product Description"
        payment_line.Amount = 100

        self.assertEquals(unicode(payment_line), "[1] Product Description 100")


class PaymentTests(unittest.TestCase):
    def test_unicode(self):
        payment = Payment()
        payment.TotalAmt = 1000

        self.assertEquals(unicode(payment), '1000')
