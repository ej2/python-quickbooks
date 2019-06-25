from datetime import datetime

from quickbooks.objects.taxservice import TaxService, TaxRateDetails
from tests.integration.test_base import QuickbooksTestCase


class TaxServiceTest(QuickbooksTestCase):
    def setUp(self):
        super(TaxServiceTest, self).setUp()

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
