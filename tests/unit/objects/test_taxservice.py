import unittest

from quickbooks.objects.taxservice import TaxService, TaxRateDetails


class TaxServiceTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxService()
        tax.TaxCode = "test"

        self.assertEquals(tax.__unicode__(), "test")


class TaxRateDetailsTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxRateDetails()
        tax.TaxRateName = "test"

        self.assertEquals(tax.__unicode__(), "test")