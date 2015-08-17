import unittest

from quickbooks.objects.taxcode import TaxCode


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        taxcode = TaxCode()
        taxcode.Name = "test"

        self.assertEquals(unicode(taxcode), "test")
