import unittest

from quickbooks.objects.tax import TaxLineDetail, TaxLine, TxnTaxDetail


class TaxLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TaxLineDetail()
        detail.TaxPercent = 10

        self.assertEquals(str(detail), "10")


class TaxLineTests(unittest.TestCase):
    def test_unicode(self):
        line = TaxLine()
        line.Amount = 100

        self.assertEquals(str(line), "100")


class TxnTaxDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = TxnTaxDetail()
        detail.TotalTax = 100

        self.assertEquals(str(detail), "100")
