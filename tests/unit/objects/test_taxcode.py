import unittest

from quickbooks.objects.taxcode import TaxCode, TaxRateDetail, TaxRateList


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        taxcode = TaxCode()
        taxcode.Name = "test"

        self.assertEquals(str(taxcode), "test")


class TaxRateDetailTests(unittest.TestCase):
    def test_init(self):
        tax_rate = TaxRateDetail()

        self.assertEquals(tax_rate.TaxOrder, 0)
        self.assertEquals(tax_rate.TaxTypeApplicable, "")


class TaxRateListTests(unittest.TestCase):
    def test_init(self):
        tax_rate_list = TaxRateList()

        self.assertEquals(tax_rate_list.TaxRateDetail, [])
