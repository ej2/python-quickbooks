import os
import unittest

from quickbooks.auth import Oauth1SessionManager
from quickbooks.objects.account import Account

from quickbooks.objects.deposit import Deposit, DepositLine, DepositLineDetail

from quickbooks import QuickBooks


class DepositTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
        )

        self.qb_client = QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id=os.environ.get('COMPANY_ID')
        )

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
