import unittest

from quickbooks import QuickBooks
from quickbooks.objects.billpayment import BillPayment, BillPaymentLine, CheckPayment, BillPaymentCreditCard


class CheckPaymentTests(unittest.TestCase):
    def test_unicode(self):
        checkpayment = CheckPayment()
        checkpayment.PrintStatus = "test"

        self.assertEquals(str(checkpayment), "test")


class BillPaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        bill = BillPaymentLine()
        bill.Amount = 1000

        self.assertEquals(str(bill), "1000")


class BillPaymentTests(unittest.TestCase):
    def test_unicode(self):
        bill_payment = BillPayment()
        bill_payment.TotalAmt = 1000

        self.assertEquals(str(bill_payment), "1000")

    def test_valid_object_name(self):
        obj = BillPayment()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class BillPaymentCreditCardTests(unittest.TestCase):
    def test_init(self):
        bill_payment_cc = BillPaymentCreditCard()

        self.assertEquals(bill_payment_cc.CCAccountRef, None)
