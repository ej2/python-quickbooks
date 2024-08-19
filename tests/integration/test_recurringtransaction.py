from datetime import datetime, timedelta
from quickbooks.objects.base import Ref
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail, AccountBasedExpenseLine, AccountBasedExpenseLineDetail
from quickbooks.objects.recurringtransaction import RecurringTransaction, RecurringInfo, ScheduleInfo, RecurringInvoice, RecurringBill
from quickbooks.objects.item import Item
from quickbooks.objects.vendor import Vendor
from tests.integration.test_base import QuickbooksTestCase


class RecurringTransactionTest(QuickbooksTestCase):
    def setUp(self):
        super(RecurringTransactionTest, self).setUp()
        self.now = datetime.now()

    def create_recurring_invoice(self, t):
        # Regular Invoice stuff except use a RecurringInvoice
        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        
        line.SalesItemLineDetail = SalesItemLineDetail()        
        item = Item.all(max_results=1, qb=self.qb_client)[0]
        line.SalesItemLineDetail.ItemRef = item.to_ref()

        invoice = RecurringInvoice()

        invoice.Line.append(line)

        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice.CustomerRef = customer.to_ref()

        # Now the recurring bits
        info = RecurringInfo()
        info.Active = True
        info.RecurType = "Automated"
        info.Name = "Test Recurring Invoice {}".format(t.strftime('%d%H%M%S'))
        
        info.ScheduleInfo = ScheduleInfo()
        info.ScheduleInfo.StartDate = t.strftime("%Y-%m-%d")
        info.ScheduleInfo.MaxOccurrences = 6
        info.ScheduleInfo.IntervalType = "Monthly"
        info.ScheduleInfo.DayOfMonth = 1
        info.ScheduleInfo.NumInterval = 1
        invoice.RecurringInfo = info

        rt = RecurringTransaction()
        rt.Invoice = invoice

        return rt.save(qb=self.qb_client)


    def test_create_recurring_invoice(self):
        actual_rt = self.create_recurring_invoice(self.now)

        self.assertTrue(hasattr(actual_rt, "Invoice"))
        self.assertEqual(actual_rt.Invoice.Line[0].Description, "description")
        self.assertEqual(actual_rt.Invoice.Line[0].Amount, 100.0)
        
        actual_info = actual_rt.Invoice.RecurringInfo
        self.assertEqual(actual_info.ScheduleInfo.MaxOccurrences, 6)
        self.assertEqual(actual_info.ScheduleInfo.IntervalType, "Monthly")
        self.assertEqual(actual_info.ScheduleInfo.DayOfMonth, 1)
        self.assertEqual(actual_info.ScheduleInfo.NumInterval, 1)

    
    def test_create_recurring_bill(self):
        bill = RecurringBill()

        line = AccountBasedExpenseLine()
        line.Amount = 500
        line.DetailType = "AccountBasedExpenseLineDetail"

        account_ref = Ref()
        account_ref.type = "Account"
        account_ref.value = 1
        line.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()
        line.AccountBasedExpenseLineDetail.AccountRef = account_ref
        bill.Line.append(line)

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        bill.VendorRef = vendor.to_ref()

        recurring_info = RecurringInfo()
        recurring_info.Active = True
        recurring_info.RecurType = "Automated"
        recurring_info.Name = "Test Recurring Bill {}".format(datetime.now().strftime('%d%H%M%S'))

        recurring_info.ScheduleInfo = ScheduleInfo()
        recurring_info.ScheduleInfo.StartDate = self.now.strftime("%Y-%m-%d")
        
        end_date = self.now + timedelta(weeks=12)
        recurring_info.ScheduleInfo.EndDate = end_date.strftime("%Y-%m-%d")

        recurring_info.ScheduleInfo.NumInterval = 1
        recurring_info.ScheduleInfo.DaysBefore = 3
        recurring_info.ScheduleInfo.IntervalType = "Weekly"
        recurring_info.ScheduleInfo.DayOfWeek = "Friday"

        bill.RecurringInfo = recurring_info

        recurring_txn = RecurringTransaction()
        recurring_txn.Bill = bill

        saved = recurring_txn.save(qb=self.qb_client)

        actual_rt = RecurringTransaction.get(saved.Bill.Id, qb=self.qb_client)
        
        self.assertTrue(hasattr(actual_rt, "Bill"))
        actual_info = actual_rt.Bill.RecurringInfo
        self.assertEqual(actual_info.ScheduleInfo.EndDate, end_date.strftime("%Y-%m-%d"))
        self.assertEqual(actual_info.ScheduleInfo.IntervalType, "Weekly")
        self.assertEqual(actual_info.ScheduleInfo.DayOfWeek, "Friday")
        self.assertEqual(actual_info.ScheduleInfo.NumInterval, 1)

    
    def test_update_recurring_invoice(self):
        saved = self.create_recurring_invoice(self.now + timedelta(seconds=+1)) # add a second to not conflict with the other test
        recurring_txn = RecurringTransaction.get(saved.Invoice.Id, qb=self.qb_client)

        recurring_txn.Invoice.RecurringInfo.ScheduleInfo.DayOfMonth = 15
        recurring_txn.Invoice.Line[0].Amount = 250

        # QBO api returns this to us as 0 but if you send it back you get an error
        recurring_txn.Invoice.Deposit = None

        recurring_txn.save(qb=self.qb_client)

        actual = RecurringTransaction.get(saved.Invoice.Id, qb=self.qb_client)
        self.assertEqual(actual.Invoice.RecurringInfo.ScheduleInfo.DayOfMonth, 15)
        self.assertEqual(actual.Invoice.Line[0].Amount, 250)


    def test_filter_by_type(self):
        recurring_txns = RecurringTransaction.where("Type = 'Bill'", qb=self.qb_client)

        for recurring_txn in recurring_txns:
            self.assertTrue(hasattr(recurring_txn, "Bill"))


    # this one is mostly to demostrate how to use this
    def test_get_all(self):
        recurring_txns = RecurringTransaction.all(qb=self.qb_client)

        self.assertGreater(len(recurring_txns), 1)

        types = set()

        for recurring_txn in recurring_txns:
            if hasattr(recurring_txn, "Invoice"):
                types.add("Invoice")
            elif hasattr(recurring_txn, "Bill"):
                types.add("Bill")
            elif hasattr(recurring_txn, "Purchase"):
                types.add("Purchase")
            # etc...

        self.assertIn("Bill", types)
        self.assertIn("Invoice", types)

    
    def test_delete_recurring_invoice(self):
        # add a second to not conflict with the other test
        saved = self.create_recurring_invoice(self.now + timedelta(seconds=+1))
        recurring_txn = RecurringTransaction.get(saved.Invoice.Id, qb=self.qb_client)

        recurring_txn.delete(qb=self.qb_client)


