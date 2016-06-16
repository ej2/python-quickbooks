import unittest

from quickbooks import QuickBooks
from quickbooks.objects.transfer import Transfer


class TaxAgencyTests(unittest.TestCase):
    def test_unicode(self):
        transfer = Transfer()
        transfer.Amount = 100

        self.assertEquals(str(transfer), "100")

    def test_valid_object_name(self):
        obj = Transfer()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
