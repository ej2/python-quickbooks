import unittest

from quickbooks.objects.creditcardpayment import CreditCardPayment, CreditChargeResponse, CreditChargeInfo


class CreditCardPaymentTests(unittest.TestCase):
    def test_init(self):
        payment = CreditCardPayment()

        self.assertEqual(payment.CreditChargeInfo, None)
        self.assertEqual(payment.CreditChargeResponse, None)


class CreditChargeResponseTests(unittest.TestCase):
    def test_init(self):
        response = CreditChargeResponse()

        self.assertEqual(response.CCTransId, "")
        self.assertEqual(response.AuthCode, "")
        self.assertEqual(response.TxnAuthorizationTime, "")
        self.assertEqual(response.Status, "")


class CreditChargeInfoTests(unittest.TestCase):
    def test_init(self):
        info = CreditChargeInfo()

        self.assertEqual(info.Type, "")
        self.assertEqual(info.NameOnAcct, "")
        self.assertEqual(info.CcExpiryMonth, 0)
        self.assertEqual(info.CcExpiryYear, 0)
        self.assertEqual(info.BillAddrStreet, "")
        self.assertEqual(info.PostalCode, "")
        self.assertEqual(info.Amount, 0)
        self.assertEqual(info.ProcessPayment, False)
