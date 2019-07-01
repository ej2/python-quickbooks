from datetime import datetime

from quickbooks.objects.base import Ref
from quickbooks.objects.bill import Bill
from quickbooks.objects.detailline import AccountBasedExpenseLine, AccountBasedExpenseLineDetail
from quickbooks.objects.vendor import Vendor
from tests.integration.test_base import QuickbooksTestCase


class BillTest(QuickbooksTestCase):
    def setUp(self):
        super(BillTest, self).setUp()
        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        bill = Bill()

        line = AccountBasedExpenseLine()
        line.Amount = 200
        line.DetailType = "AccountBasedExpenseLineDetail"

        account_ref = Ref()
        account_ref.type = "Account"
        account_ref.value = 1
        line.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()
        line.AccountBasedExpenseLineDetail.AccountRef = account_ref
        bill.Line.append(line)

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        bill.VendorRef = vendor.to_ref()

        bill.save(qb=self.qb_client)

        query_bill = Bill.get(bill.Id, qb=self.qb_client)

        self.assertEquals(query_bill.Id, bill.Id)
        self.assertEquals(len(query_bill.Line), 1)
        self.assertEquals(query_bill.Line[0].Amount, 200.0)
