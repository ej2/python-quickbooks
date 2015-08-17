import unittest

from quickbooks.objects.billpayment import BillPayment, BillPaymentLine, CheckPayment


class CheckPaymentTests(unittest.TestCase):
    def test_unicode(self):
        checkpayment = CheckPayment()
        checkpayment.PrintStatus = "test"

        self.assertEquals(unicode(checkpayment), "test")


class BillPaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        bill = BillPaymentLine()
        bill.Amount = 1000

        self.assertEquals(unicode(bill), "1000")


class BillPaymentTests(unittest.TestCase):
    def test_unicode(self):
        bill_payment = BillPayment()
        bill_payment.TotalAmt = 1000

        self.assertEquals(unicode(bill_payment), "1000")
