import unittest

from quickbooks import QuickBooks
from quickbooks.objects.creditcardpayment_entity import CreditCardPayment


class TaxAgencyTests(unittest.TestCase):
    def test_unicode(self):
        credit_card_payment = CreditCardPayment()
        credit_card_payment.Amount = 100

        self.assertEquals(str(credit_card_payment), "100")

    def test_valid_object_name(self):
        obj = CreditCardPayment()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
