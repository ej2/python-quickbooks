from datetime import datetime

from quickbooks.objects import AccountBasedExpenseLine, Ref, AccountBasedExpenseLineDetail
from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.billpayment import BillPayment, BillPaymentLine, CheckPayment
from quickbooks.objects.vendor import Vendor
from tests.integration.test_base import QuickbooksTestCase


class BillPaymentTest(QuickbooksTestCase):
    def setUp(self):
        super(BillPaymentTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def create_bill(self, amount):
        bill = Bill()
        line = AccountBasedExpenseLine()
        line.Amount = amount
        line.DetailType = "AccountBasedExpenseLineDetail"

        account_ref = Ref()
        account_ref.type = "Account"
        account_ref.value = 1
        line.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()
        line.AccountBasedExpenseLineDetail.AccountRef = account_ref
        bill.Line.append(line)

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        bill.VendorRef = vendor.to_ref()

        return bill.save(qb=self.qb_client)

    def create_bill_payment(self, bill, amount, private_note, pay_type):
        bill_payment = BillPayment()

        bill_payment.PayType = pay_type
        bill_payment.TotalAmt = amount
        bill_payment.PrivateNote = private_note

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        bill_payment.VendorRef = vendor.to_ref()

        bill_payment.CheckPayment = CheckPayment()
        account = Account.where("AccountSubType = 'Checking'", qb=self.qb_client)[0]
        bill_payment.CheckPayment.BankAccountRef = account.to_ref()

        ap_account = Account.where("AccountSubType = 'AccountsPayable'", qb=self.qb_client)[0]
        bill_payment.APAccountRef = ap_account.to_ref()

        line = BillPaymentLine()
        line.LinkedTxn.append(bill.to_linked_txn())
        line.Amount = 200

        bill_payment.Line.append(line)
        return bill_payment.save(qb=self.qb_client)

    def test_create(self):
        # create new bill for testing, reusing the same bill will cause Line to be empty
        # and the new bill payment will be voided automatically
        bill = self.create_bill(amount=200)
        bill_payment = self.create_bill_payment(bill, 200, "Private Note", "Check")

        query_bill_payment = BillPayment.get(bill_payment.Id, qb=self.qb_client)

        self.assertEqual(query_bill_payment.PayType, "Check")
        self.assertEqual(query_bill_payment.TotalAmt, 200.0)
        self.assertEqual(query_bill_payment.PrivateNote, "Private Note")

        self.assertEqual(len(query_bill_payment.Line), 1)
        self.assertEqual(query_bill_payment.Line[0].Amount, 200.0)

    def test_void(self):
        bill = self.create_bill(amount=200)
        bill_payment = self.create_bill_payment(bill, 200, "Private Note", "Check")
        query_payment = BillPayment.get(bill_payment.Id, qb=self.qb_client)
        self.assertEqual(query_payment.TotalAmt, 200.0)
        self.assertNotIn('Voided', query_payment.PrivateNote)

        bill_payment.void(qb=self.qb_client)
        query_payment = BillPayment.get(bill_payment.Id, qb=self.qb_client)

        self.assertEqual(query_payment.TotalAmt, 0.0)
        self.assertIn('Voided', query_payment.PrivateNote)