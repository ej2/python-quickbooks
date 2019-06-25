from datetime import datetime

from quickbooks.objects.companycurrency import CompanyCurrency
from tests.integration.test_base import QuickbooksUnitTestCase


class CompanyCurrencyTest(QuickbooksUnitTestCase):
    def test_unicode(self):
        company_currency = CompanyCurrency()
        company_currency.Name = "test"
        company_currency.Code = "USD"

        self.assertEquals(str(company_currency), "test")

    def test_to_ref(self):
        company_currency = CompanyCurrency()
        company_currency.Name = "test"
        company_currency.Id = 23

        ref = company_currency.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "CompanyCurrency")
        self.assertEquals(ref.value, 23)