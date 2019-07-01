from quickbooks.objects.taxcode import TaxCode
from tests.integration.test_base import QuickbooksTestCase


class TaxCodeTest(QuickbooksTestCase):
    def test_get_all(self):
        tax_codes = TaxCode.all(max_results=1, qb=self.qb_client)

        # KNOWN Quickbooks bug - TaxCode query returns 3 extra items:
        # https://intuitdeveloper.lc.intuit.com/questions/1398164-setting-maxresults-on-taxcode-query-returns-incorrect-number-of-records

        self.assertEquals(len(tax_codes), 4)

