import unittest

from quickbooks import QuickBooks
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

    def test_valid_object_name(self):
        obj = Payment()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)