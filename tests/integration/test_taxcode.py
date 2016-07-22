import os
import unittest

from quickbooks.client import QuickBooks
from quickbooks.objects.taxcode import TaxCode


class TaxCodeTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

    def test_get_all(self):
        tax_codes = TaxCode.all(max_results=1, qb=self.qb_client)

        # KNOWN Quickbooks bug - TaxCode query returns 3 extra items:
        # https://intuitdeveloper.lc.intuit.com/questions/1398164-setting-maxresults-on-taxcode-query-returns-incorrect-number-of-records

        self.assertEquals(len(tax_codes), 4)

