import unittest

from quickbooks.objects.taxservice import TaxService, TaxRateDetails


class TaxServiceTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxService()
        tax.TaxCode = "test"

        self.assertEquals(str(tax), "test")


class TaxRateDetailsTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxRateDetails()
        tax.TaxRateName = "test"

        self.assertEquals(str(tax), "test")