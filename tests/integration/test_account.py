from datetime import datetime
from quickbooks.objects.account import Account
from tests.integration.test_base import QuickbooksTestCase


class AccountTest(QuickbooksTestCase):
    def setUp(self):
        super(AccountTest, self).setUp()

        self.time = datetime.now()
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

        self.assertEqual(account.Id, query_account.Id)
        self.assertEqual(query_account.Name, self.name)
        self.assertEqual(query_account.AcctNum, self.account_number)

    def test_update(self):
        account = Account.filter(Name=self.name, qb=self.qb_client)[0]

        account.Name = "Updated Name {0}".format(self.account_number)
        account.save(qb=self.qb_client)

        query_account = Account.get(account.Id, qb=self.qb_client)
        self.assertEqual(query_account.Name, "Updated Name {0}".format(self.account_number))

    def test_create_using_from_json(self):
        account = Account.from_json({
            "AcctNum": datetime.now().strftime('%d%H%M%S'),
            "Name": "{} {}".format(self.name, self.time.strftime("%Y-%m-%d %H:%M:%S")),
            "AccountSubType": "CashOnHand"
        })

        account.save(qb=self.qb_client)
