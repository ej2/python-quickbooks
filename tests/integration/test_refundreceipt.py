from datetime import datetime

from quickbooks.objects import RefundReceipt, DetailLine, CustomerMemo, SalesItemLineDetail, \
    Account, Item
from quickbooks.objects.refundreceipt import RefundReceiptCheckPayment
from tests.integration.test_base import QuickbooksTestCase


class PaymentTest(QuickbooksTestCase):
    def setUp(self):
        super(PaymentTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        refund_receipt = RefundReceipt()
        refund_receipt.DocNumber = "DocNum123"
        refund_receipt.TotalAmt = 100
        refund_receipt.Balance = 100
        refund_receipt.PrivateNote = "Private Note"
        refund_receipt.PaymentType = "Check"

        memo = CustomerMemo()
        memo.value = "Customer Memo"
        refund_receipt.CustomerMemo = memo

        refund_receipt.CheckPayment = RefundReceiptCheckPayment()
        refund_receipt.CheckPayment.CheckNum = "1001"
        refund_receipt.CheckPayment.NameOnAcct = "John Smith"
        refund_receipt.CheckPayment.AcctNum = "0000000000"
        refund_receipt.CheckPayment.BankName = "Bank"

        item = Item.all(max_results=1, qb=self.qb_client)[0]
        line = DetailLine()
        line.DetailType = "SalesItemLineDetail"
        line.Amount = 200
        line.SalesItemLineDetail = SalesItemLineDetail()
        line.SalesItemLineDetail.ItemRef = item.to_ref()
        refund_receipt.Line.append(line)

        account = Account.where("Name = 'checking'", max_results=1, qb=self.qb_client)[0]
        refund_receipt.DepositToAccountRef = account.to_ref()

        refund_receipt.save(qb=self.qb_client)

        query_refund_receipt = RefundReceipt.get(refund_receipt.Id, qb=self.qb_client)

        self.assertEqual(query_refund_receipt.DocNumber, refund_receipt.DocNumber)
        self.assertEqual(query_refund_receipt.Line[0].Amount, 200)
        self.assertEqual(refund_receipt.DepositToAccountRef.value, account.Id)
