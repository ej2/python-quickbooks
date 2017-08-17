from datetime import datetime
import os
import unittest

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account


class AccountTest(unittest.TestCase):
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

    # def test_temp(self):
    #     session_manager = Oauth1SessionManager(
    #         sandbox=True,
    #         consumer_key=os.environ.get('CONSUMER_KEY'),
    #         consumer_secret=os.environ.get('CONSUMER_SECRET'),
    #         callback_url='http://localhost:8000'
    #     )
    #
    #     authorize_url = session_manager.get_authorize_url()
    #
    #     print authorize_url
    #     print session_manager.request_token
    #     print session_manager.request_token_secret
    #
    #     session_manager.authorize_url = authorize_url
    #     #session_manager.request_token = request_token
    #     #session_manager.request_token_secret = request_token_secret
    #     session_manager.set_up_service()
    #
    #     session_manager.get_access_tokens(request.GET['oauth_verifier'])
    #
    #     realm_id = request.GET['realmId']
    #     access_token = client.access_token
    #     access_token_secret = client.access_token_secret
