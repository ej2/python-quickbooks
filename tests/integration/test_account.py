from datetime import datetime
import os
import unittest

from quickbooks.auth import Oauth2SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account


class AccountTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth2SessionManager(
            sandbox=True,
            client_id=os.environ.get('CLIENT_ID'),
            client_secret=os.environ.get('CLIENT_SECRET'),
            access_token=os.environ.get('AUTH2_ACCESS_TOKEN'),
        )

        self.qb_client = QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id=os.environ.get('COMPANY_ID2')
        )

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        account = Account()
        account.AcctNum = self.account_number
        account.Name = self.name
        account.AccountSubType = "CashOnHand"
        account.save(qb=self.qb_client)

        self.id = account.Id
        query_account = Account.get(account.Id, qb=self.qb_client)

        self.assertEquals(account.Id, query_account.Id)
        self.assertEquals(query_account.Name, self.name)
        self.assertEquals(query_account.AcctNum, self.account_number)

    def test_update(self):
        account = Account.filter(Name=self.name, qb=self.qb_client)[0]

        account.Name = "Updated Name {0}".format(self.account_number)
        account.save(qb=self.qb_client)

        query_account = Account.get(account.Id, qb=self.qb_client)
        self.assertEquals(query_account.Name, "Updated Name {0}".format(self.account_number))
