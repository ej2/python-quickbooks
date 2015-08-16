import unittest

from quickbooks.objects.tax import TaxLineDetail, TaxLine, TxnTaxDetail


class TaxLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TaxLineDetail()
        detail.TaxPercent = 10

        self.assertEquals(detail.__unicode__(), 10)


class TaxLineTests(unittest.TestCase):
    def test_unicode(self):
        line = TaxLine()
        line.Amount = 100

        self.assertEquals(line.__unicode__(), 100)


class TxnTaxDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TxnTaxDetail()
        detail.TotalTax = 100

        self.assertEquals(detail.__unicode__(), 100)
