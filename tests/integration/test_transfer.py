import time
from datetime import datetime

from quickbooks.objects.account import Account
from quickbooks.objects.transfer import Transfer
from tests.integration.test_base import QuickbooksTestCase


class TransferTest(QuickbooksTestCase):
    def setUp(self):
        time.sleep(3)  # Used to prevent error code 3001 - The request limit was reached.
        super(TransferTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Transfer {0}".format(self.account_number)

    def test_create(self):
        accounts = Account.where(
            "Classification = 'Asset' AND FullyQualifiedName != 'Accounts Receivable (A/R)'",
            max_results=2, qb=self.qb_client)

        from_account = accounts[0]
        to_account = accounts[1]

        transfer = Transfer()
        transfer.Amount = 100
        transfer.FromAccountRef = from_account.to_ref()
        transfer.ToAccountRef = to_account.to_ref()

        transfer.save(qb=self.qb_client)

        query_transfer = Transfer.get(transfer.Id, qb=self.qb_client)

        self.assertEquals(query_transfer.Id, transfer.Id)
        self.assertEquals(query_transfer.Amount, 100)
        self.assertEquals(query_transfer.FromAccountRef.value, from_account.Id)
        self.assertEquals(query_transfer.ToAccountRef.value, to_account.Id)

        # reset transfer (so the from_account doesn't run out of cash)
        transfer = Transfer()
        transfer.Amount = 100
        transfer.FromAccountRef = to_account.to_ref()
        transfer.ToAccountRef = from_account.to_ref()

        transfer.save(qb=self.qb_client)

    def test_update(self):
        transfer = Transfer.all(max_results=1, qb=self.qb_client)[0]
        transfer.Amount += 1
        transfer.save(qb=self.qb_client)

        query_transfer = Transfer.get(transfer.Id, qb=self.qb_client)

        self.assertEquals(query_transfer.Amount, transfer.Amount)
