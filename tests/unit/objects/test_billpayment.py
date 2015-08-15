import unittest

from quickbooks.objects.billpayment import BillPayment, BillPaymentLine, CheckPayment


class CheckPaymentTests(unittest.TestCase):
    def test_unicode(self):
        checkpayment = CheckPayment()
        checkpayment.PrintStatus = "test"

        self.assertEquals(checkpayment.__unicode__(), "test")


class BillPaymentLineTests(unittest.TestCase):
    def test_unicode(self):
        bill = BillPaymentLine()
        bill.Amount = 1000

        self.assertEquals(bill.__unicode__(), 1000)


class BillPaymentTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        bill_payment = BillPayment()
        bill_payment.TotalAmt = 1000

        self.assertEquals(bill_payment.__unicode__(), 1000)
