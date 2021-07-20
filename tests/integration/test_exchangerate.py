from datetime import datetime
from quickbooks.objects.exchangerate import ExchangeRate
from tests.integration.test_base import QuickbooksTestCase


class ExchangeRateTest(QuickbooksTestCase):
    def test_query(self):
        exchange_rate = ExchangeRate.where("SourceCurrencyCode = 'EUR'", qb=self.qb_client)[0]

        self.assertEquals(exchange_rate.SourceCurrencyCode, "EUR")
        self.assertEquals(exchange_rate.TargetCurrencyCode, "USD")

    def test_update(self):
        exchange_rate = ExchangeRate.where("SourceCurrencyCode = 'EUR'", qb=self.qb_client)[0]

        new_rate = exchange_rate.Rate + 1
        exchange_rate.Rate = new_rate
        exchange_rate.save(qb=self.qb_client)

        exchange_rate_updated = ExchangeRate.where("SourceCurrencyCode = 'EUR'", qb=self.qb_client)[0]
        self.assertEquals(exchange_rate_updated.Rate, new_rate)
