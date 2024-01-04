from datetime import datetime

from quickbooks.objects.base import Ref, Address
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

        # Test undocumented VendorAddr field
        bill.VendorAddr = Address()
        bill.VendorAddr.Line1 = "123 Main"
        bill.VendorAddr.Line2 = "Apartment 1"
        bill.VendorAddr.City = "City"
        bill.VendorAddr.Country = "U.S.A"
        bill.VendorAddr.CountrySubDivisionCode = "CA"
        bill.VendorAddr.PostalCode = "94030"

        bill.save(qb=self.qb_client)

        query_bill = Bill.get(bill.Id, qb=self.qb_client)

        self.assertEqual(query_bill.Id, bill.Id)
        self.assertEqual(len(query_bill.Line), 1)
        self.assertEqual(query_bill.Line[0].Amount, 200.0)

        self.assertEqual(query_bill.VendorAddr.Line1, bill.VendorAddr.Line1)
        self.assertEqual(query_bill.VendorAddr.Line2, bill.VendorAddr.Line2)
        self.assertEqual(query_bill.VendorAddr.City, bill.VendorAddr.City)
        self.assertEqual(query_bill.VendorAddr.Country, bill.VendorAddr.Country)
        self.assertEqual(query_bill.VendorAddr.CountrySubDivisionCode, bill.VendorAddr.CountrySubDivisionCode)
        self.assertEqual(query_bill.VendorAddr.PostalCode, bill.VendorAddr.PostalCode)



