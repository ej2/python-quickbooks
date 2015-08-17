import unittest

from quickbooks.objects.tax import TaxLineDetail, TaxLine, TxnTaxDetail


class TaxLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TaxLineDetail()
        detail.TaxPercent = 10

        self.assertEquals(unicode(detail), "10")


class TaxLineTests(unittest.TestCase):
    def test_unicode(self):
        line = TaxLine()
        line.Amount = 100

        self.assertEquals(unicode(line), "100")


class TxnTaxDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TxnTaxDetail()
        detail.TotalTax = 100

        self.assertEquals(unicode(detail), "100")
