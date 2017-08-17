import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.taxservice import TaxService, TaxRateDetails


class TaxServiceTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
        )

        self.qb_client = QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id=os.environ.get('COMPANY_ID')
        )

        self.name = "TaxCode {0}".format(datetime.now().strftime('%d%H%M'))

    def test_create(self):
        taxservice = TaxService()
        taxservice.TaxCode = self.name
        tax_rate_detail = TaxRateDetails()

        tax_rate_detail.TaxRateName = self.name
        tax_rate_detail.RateValue = 10
        tax_rate_detail.TaxAgencyId = 1
        tax_rate_detail.TaxApplicableOn = "Sales"

        taxservice.TaxRateDetails.append(tax_rate_detail)

        created_taxservice = taxservice.save(qb=self.qb_client)

        self.assertEquals(created_taxservice.TaxCode, self.name)

        detail = created_taxservice.TaxRateDetails[0]
        self.assertEquals(detail.TaxRateName, self.name)
        self.assertEquals(detail.RateValue, 10)
        self.assertEquals(detail.TaxAgencyId, '1')
        self.assertEquals(detail.TaxApplicableOn, "Sales")
