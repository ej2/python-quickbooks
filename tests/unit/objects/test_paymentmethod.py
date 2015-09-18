import unittest

from quickbooks.objects.paymentmethod import PaymentMethod


class PaymentMethodTests(unittest.TestCase):
    def test_unicode(self):
        payment_method = PaymentMethod()
        payment_method.Name = "test"

        self.assertEquals(str(payment_method), "test")
