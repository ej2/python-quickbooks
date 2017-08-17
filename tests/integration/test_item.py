import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account
from quickbooks.objects.item import Item


class ItemTest(unittest.TestCase):
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
        self.name = "Test Item {0}".format(self.account_number)

        self.income_account = Account.where(
            "AccountType = 'Income' and AccountSubType = 'SalesOfProductIncome'", max_results=1, qb=self.qb_client)[0]

        self.expense_account = Account.where(
            "AccountSubType = 'SuppliesMaterialsCogs'", max_results=1, qb=self.qb_client)[0]
        self.asset_account = Account.where("AccountSubType = 'Inventory'", max_results=1, qb=self.qb_client)[0]

    def test_create(self):
        item = Item()

        item.Name = self.name
        item.Type = "Inventory"
        item.TrackQtyOnHand = True
        item.QtyOnHand = 10
        item.InvStartDate = "2015-01-01"

        item.IncomeAccountRef = self.income_account.to_ref()
        item.ExpenseAccountRef = self.expense_account.to_ref()
        item.AssetAccountRef = self.asset_account.to_ref()
        item.save(qb=self.qb_client)

        query_item = Item.get(item.Id, qb=self.qb_client)

        self.assertEquals(query_item.Id, item.Id)
        self.assertEquals(query_item.Name, self.name)
        self.assertEquals(query_item.Type, "Inventory")
        self.assertEquals(query_item.TrackQtyOnHand, True)
        self.assertEquals(query_item.QtyOnHand, 10)
        self.assertEquals(query_item.IncomeAccountRef.value, self.income_account.Id)
        self.assertEquals(query_item.ExpenseAccountRef.value, self.expense_account.Id)
        self.assertEquals(query_item.AssetAccountRef.value, self.asset_account.Id)
