import unittest

from quickbooks import QuickBooks
from quickbooks.objects.taxrate import TaxRate


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxRate()
        tax.Name = "test"

        self.assertEquals(str(tax), "test")

    def test_valid_object_name(self):
        obj = TaxRate()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
