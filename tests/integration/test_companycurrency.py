from quickbooks.objects import Customer
from quickbooks.objects.companycurrency import CompanyCurrency
from tests.integration.test_base import QuickbooksTestCase


class CompanyCurrencyTest(QuickbooksTestCase):
    def test_get_all(self):
        currencies = CompanyCurrency.all(qb=self.qb_client)
        self.assertGreater(len(currencies), 0)

    def test_get(self):
        currency = CompanyCurrency.get(id=1, qb=self.qb_client)
        self.assertEqual(currency.Name, 'Canadian Dollar')
