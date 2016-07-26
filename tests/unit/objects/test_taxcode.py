import unittest

from quickbooks import QuickBooks
from quickbooks.objects.taxcode import TaxCode, TaxRateDetail, TaxRateList


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        taxcode = TaxCode()
        taxcode.Name = "test"

        self.assertEquals(str(taxcode), "test")

    def test_valid_object_name(self):
        obj = TaxCode()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        taxcode = TaxCode()
        taxcode.Name = "test"

        ref = taxcode.to_ref()
        self.assertEquals(ref.value, "test")


class TaxRateDetailTests(unittest.TestCase):
    def test_init(self):
        tax_rate = TaxRateDetail()

        self.assertEquals(tax_rate.TaxOrder, 0)
        self.assertEquals(tax_rate.TaxTypeApplicable, "")


class TaxRateListTests(unittest.TestCase):
    def test_init(self):
        tax_rate_list = TaxRateList()

        self.assertEquals(tax_rate_list.TaxRateDetail, [])
