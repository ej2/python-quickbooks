import unittest

from quickbooks import QuickBooks
from quickbooks.objects.exchangerate import ExchangeRate, ExchangeRateMetaData


class ExchangeRateTests(unittest.TestCase):
    def test_unicode(self):
        exchange_rate = ExchangeRate()
        exchange_rate.SourceCurrencyCode = "EUR"

        exchange_rate.MetaData = ExchangeRateMetaData()
        exchange_rate.MetaData.LastUpdatedTime = "1"

        self.assertEqual(str(exchange_rate), "EUR")
        self.assertEqual(exchange_rate.MetaData.LastUpdatedTime, "1")

    def test_valid_object_name(self):
        obj = ExchangeRate()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
