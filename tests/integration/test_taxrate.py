import os
import unittest

from quickbooks.client import QuickBooks
from quickbooks.objects.taxrate import TaxRate


class TaxRateTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

    def test_read(self):
        tax_rates = TaxRate.all(max_results=1, qb=self.qb_client)

        self.assertEquals(len(tax_rates), 1)

