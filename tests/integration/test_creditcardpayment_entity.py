import time
from datetime import datetime

from quickbooks.objects import Transfer
from quickbooks.objects.account import Account
from quickbooks.objects.creditcardpayment_entity import CreditCardPayment
from tests.integration.test_base import QuickbooksTestCase


class CreditCardPaymentEntityTest(QuickbooksTestCase):
    def setUp(self):
        time.sleep(3)  # Used to prevent error code 3001 - The request limit was reached.
        super(CreditCardPaymentEntityTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test CreditCardPaymentEntityTest {0}".format(self.account_number)

    def test_create(self):
        credit_card_account = Account()
        credit_card_account.Name = "Credit Card Account {0}".format(self.account_number)
        credit_card_account.AccountType = "Credit Card"
        credit_card_account.AccountSubType = "CreditCard"
        credit_card_account.save(qb=self.qb_client)

        accounts = Account.where(
            "Classification = 'Asset' AND FullyQualifiedName != 'Accounts Receivable (A/R)'",
            max_results=1, qb=self.qb_client)

        from_account = accounts[0]
        to_account = credit_card_account

        credit_card_payment = CreditCardPayment()
        credit_card_payment.Amount = 100
        credit_card_payment.BankAccountRef = from_account.to_ref()
        credit_card_payment.CreditCardAccountRef = to_account.to_ref()

        credit_card_payment.save(qb=self.qb_client)

        query_credit_card_payment = CreditCardPayment.get(credit_card_payment.Id, qb=self.qb_client)

        self.assertEquals(query_credit_card_payment.Id, credit_card_payment.Id)
        self.assertEquals(query_credit_card_payment.Amount, 100)
        self.assertEquals(query_credit_card_payment.BankAccountRef.value, from_account.Id)
        self.assertEquals(query_credit_card_payment.CreditCardAccountRef.value, to_account.Id)

        # reset transfer (so the from_account doesn't run out of cash)
        # I wonder if we can do a transfer from credit_card_account to a bank_account
        transfer = Transfer()
        transfer.Amount = 100
        transfer.FromAccountRef = to_account.to_ref()
        transfer.ToAccountRef = from_account.to_ref()

        transfer.save(qb=self.qb_client)

    def test_update(self):
        credit_card_payment = CreditCardPayment.all(max_results=1, qb=self.qb_client)[0]
        credit_card_payment.Amount += 1
        credit_card_payment.save(qb=self.qb_client)

        query_credit_card_payment = CreditCardPayment.get(credit_card_payment.Id, qb=self.qb_client)

        self.assertEquals(query_credit_card_payment.Amount, credit_card_payment.Amount)
