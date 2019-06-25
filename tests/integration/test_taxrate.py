from quickbooks.objects.taxrate import TaxRate
from tests.integration.test_base import QuickbooksTestCase


class TaxRateTest(QuickbooksTestCase):
    def test_read(self):
        tax_rates = TaxRate.all(max_results=1, qb=self.qb_client)

        self.assertEquals(len(tax_rates), 1)

