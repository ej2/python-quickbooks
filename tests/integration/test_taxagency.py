from datetime import datetime

from quickbooks.objects.taxagency import TaxAgency
from tests.integration.test_base import QuickbooksTestCase


class TaxAgencyTest(QuickbooksTestCase):
    def test_read(self):
        tax_agencies = TaxAgency.all(max_results=1, qb=self.qb_client)

        self.assertEquals(len(tax_agencies), 1)

    def test_create(self):
        tax_agency = TaxAgency()

        name = "Tax Agency {0}".format(datetime.now().strftime('%d%H%M'))

        tax_agency.DisplayName = name
        tax_agency.save(qb=self.qb_client)

        query_tax_agency = TaxAgency.get(tax_agency.Id, qb=self.qb_client)

        self.assertEquals(query_tax_agency.Id, tax_agency.Id)
        self.assertEquals(query_tax_agency.DisplayName, name)