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
        # Use shorter timestamp for uniqueness (within 20 char limit)
        timestamp = datetime.now().strftime('%m%d%H%M%S')
        unique_number = f"T{timestamp}"  # T for Test
        unique_name = f"Test Account {timestamp}"
        
        account.AcctNum = unique_number
        account.Name = unique_name
        account.AccountType = "Bank"  # Required field
        account.AccountSubType = "CashOnHand"

        created_account = account.save(qb=self.qb_client)

        # Verify the save was successful
        self.assertIsNotNone(created_account)
        self.assertIsNotNone(created_account.Id)
        self.assertTrue(int(created_account.Id) > 0)

        query_account = Account.get(created_account.Id, qb=self.qb_client)

        self.assertEqual(created_account.Id, query_account.Id)
        self.assertEqual(query_account.Name, unique_name)
        self.assertEqual(query_account.AcctNum, unique_number)
        self.assertEqual(query_account.AccountType, "Bank")
        self.assertEqual(query_account.AccountSubType, "CashOnHand")

    def test_update(self):
        # First create an account with a unique name and number
        timestamp = datetime.now().strftime('%m%d%H%M%S')
        unique_number = f"T{timestamp}"
        unique_name = f"Test Account {timestamp}"
        
        account = Account()
        account.AcctNum = unique_number
        account.Name = unique_name
        account.AccountType = "Bank"
        account.AccountSubType = "CashOnHand"

        created_account = account.save(qb=self.qb_client)
        
        # Verify the save was successful
        self.assertIsNotNone(created_account)
        self.assertIsNotNone(created_account.Id)

        # Change the name
        updated_name = f"{unique_name}_updated"
        created_account.Name = updated_name
        updated_account = created_account.save(qb=self.qb_client)

        # Query the account and make sure it has changed
        query_account = Account.get(updated_account.Id, qb=self.qb_client)
        self.assertEqual(query_account.Name, updated_name)
        self.assertEqual(query_account.AcctNum, unique_number)  # Account number should not change

    def test_create_using_from_json(self):
        timestamp = datetime.now().strftime('%m%d%H%M%S')
        unique_number = f"T{timestamp}"
        unique_name = f"Test JSON {timestamp}"
        
        account = Account.from_json({
            "AcctNum": unique_number,
            "Name": unique_name,
            "AccountType": "Bank",
            "AccountSubType": "CashOnHand"
        })

        created_account = account.save(qb=self.qb_client)
        self.assertIsNotNone(created_account)
        self.assertIsNotNone(created_account.Id)

        # Verify we can get the account
        query_account = Account.get(created_account.Id, qb=self.qb_client)
        self.assertEqual(query_account.Name, unique_name)
        self.assertEqual(query_account.AccountType, "Bank")
        self.assertEqual(query_account.AccountSubType, "CashOnHand")
