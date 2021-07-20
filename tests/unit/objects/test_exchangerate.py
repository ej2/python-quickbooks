import unittest

from quickbooks import QuickBooks
from quickbooks.objects.exchangerate import ExchangeRate


class ExchangeRateTests(unittest.TestCase):
    def test_unicode(self):
        exchange_rate = ExchangeRate()
        exchange_rate.SourceCurrencyCode = "EUR"

        self.assertEquals(str(exchange_rate), "EUR")

    def test_valid_object_name(self):
        obj = ExchangeRate()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
