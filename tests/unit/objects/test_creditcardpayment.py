import unittest

from quickbooks.objects.creditcardpayment import CreditCardPayment, CreditChargeResponse, CreditChargeInfo


class CreditCardPaymentTests(unittest.TestCase):
    def test_init(self):
        payment = CreditCardPayment()

        self.assertEquals(payment.CreditChargeInfo, None)
        self.assertEquals(payment.CreditChargeResponse, None)


class CreditChargeResponseTests(unittest.TestCase):
    def test_init(self):
        response = CreditChargeResponse()

        self.assertEquals(response.CCTransId, "")
        self.assertEquals(response.AuthCode, "")
        self.assertEquals(response.TxnAuthorizationTime, "")
        self.assertEquals(response.Status, "")


class CreditChargeInfoTests(unittest.TestCase):
    def test_init(self):
        info = CreditChargeInfo()

        self.assertEquals(info.Type, "")
        self.assertEquals(info.NameOnAcct, "")
        self.assertEquals(info.CcExpiryMonth, 0)
        self.assertEquals(info.CcExpiryYear, 0)
        self.assertEquals(info.BillAddrStreet, "")
        self.assertEquals(info.PostalCode, "")
        self.assertEquals(info.Amount, 0)
        self.assertEquals(info.ProcessPayment, False)
