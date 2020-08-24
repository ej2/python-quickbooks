from datetime import datetime

from quickbooks.objects import Customer, PaymentMethod
from quickbooks.objects.account import Account
from quickbooks.objects.payment import Payment

from tests.integration.test_base import QuickbooksTestCase


class PaymentTest(QuickbooksTestCase):
    def setUp(self):
        super(PaymentTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_getall(self):
        payments = Payment.all(max_results=5, qb=self.qb_client)

        self.assertEqual(len(payments), 5)
        self.assertNotEqual(payments[0].Id, 0)

    def test_create(self):
        payment = Payment()
        payment.TotalAmt = 140.0

        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        payment.CustomerRef = customer.to_ref()

        payment_method = PaymentMethod.all(max_results=1, qb=self.qb_client)[0]

        payment.PaymentMethodRef = payment_method.to_ref()
        payment.save(qb=self.qb_client)

        query_payment = Payment.get(payment.Id, qb=self.qb_client)

        self.assertEqual(query_payment.CustomerRef.name, customer.DisplayName)
        self.assertEqual(query_payment.TotalAmt, 140.0)
        self.assertEqual(query_payment.PaymentMethodRef.value, payment_method.Id)
