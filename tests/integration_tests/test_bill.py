import unittest
from datetime import datetime

from quickbooks.objects.base import Ref
from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail
from quickbooks.objects.vendor import Vendor


class BillTest(unittest.TestCase):
    def setUp(self):

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        bill = Bill()

        line = BillLine()
        line.Amount = 200
        line.DetailType = "AccountBasedExpenseLineDetail"

        account_ref = Ref()
        account_ref.type = "Account"
        account_ref.value = 1
        line.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()
        line.AccountBasedExpenseLineDetail.AccountRef = account_ref
        bill.Line.append(line)

        vendor = Vendor.all(max_results=1)[0]
        bill.VendorRef = vendor.to_ref()

        bill.save()

        query_bill = Bill.get(bill.Id)

        self.assertEquals(query_bill.Id, bill.Id)
        self.assertEquals(len(query_bill.Line), 1)
        self.assertEquals(query_bill.Line[0].Amount, 200.0)

    def test_update(self):
        pass
