import unittest

from quickbooks.objects.payment import PaymentLine, Payment


class PaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        payment_line = PaymentLine()
        payment_line.Amount = 100

        self.assertEquals(str(payment_line), "100")


class PaymentTests(unittest.TestCase):
    def test_unicode(self):
        payment = Payment()
        payment.TotalAmt = 1000

        self.assertEquals(str(payment), '1000')
