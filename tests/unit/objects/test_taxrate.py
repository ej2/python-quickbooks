import unittest

from quickbooks.objects.taxrate import TaxRate


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        tax = TaxRate()
        tax.Name = "test"

        self.assertEquals(str(tax), "test")
