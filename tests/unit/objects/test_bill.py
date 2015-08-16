import unittest

from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        acct_detail = AccountBasedExpenseLineDetail()
        acct_detail.BillableStatus = "test"

        self.assertEquals(acct_detail.__unicode__(), "test")


class BillTests(unittest.TestCase):
    def test_unicode(self):
        bill = Bill()
        bill.Balance = 1000

        self.assertEquals(bill.__unicode__(), 1000)


class BillLineTests(unittest.TestCase):
    def test_unicode(self):
        bill_line = BillLine()
        bill_line.Amount = 1000

        self.assertEquals(bill_line.__unicode__(), 1000)
