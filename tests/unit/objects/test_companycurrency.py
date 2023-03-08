from datetime import datetime

from quickbooks.objects.companycurrency import CompanyCurrency
from tests.integration.test_base import QuickbooksUnitTestCase


class CompanyCurrencyTest(QuickbooksUnitTestCase):
    def test_unicode(self):
        company_currency = CompanyCurrency()
        company_currency.Name = "test"
        company_currency.Code = "USD"

        self.assertEqual(str(company_currency), "test")

    def test_to_ref(self):
        company_currency = CompanyCurrency()
        company_currency.Name = "test"
        company_currency.Id = 23

        ref = company_currency.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "CompanyCurrency")
        self.assertEqual(ref.value, 23)