from quickbooks.objects.account import Account
from quickbooks.objects.deposit import Deposit, DepositLine, DepositLineDetail
from tests.integration.test_base import QuickbooksTestCase


class DepositTest(QuickbooksTestCase):
    def test_create(self):
        deposit = Deposit()
        account = Account.filter(AccountType="Bank", max_results=2, qb=self.qb_client)

        account_ref = account[0].to_ref()
        deposit_to_account_ref = account[1].to_ref()

        deposit_line_detail = DepositLineDetail()
        deposit_line_detail.AccountRef = account_ref

        line = DepositLine()
        line.Amount = 20.00
        line.DetailType = "DepositLineDetail"
        line.DepositLineDetail = deposit_line_detail

        deposit.DepositToAccountRef = deposit_to_account_ref
        deposit.Line.append(line)

        deposit.save(qb=self.qb_client)

        query_deposit = Deposit.get(deposit.Id, qb=self.qb_client)

        self.assertEqual(deposit.Id, query_deposit.Id)
