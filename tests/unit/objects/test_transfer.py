import unittest

from quickbooks.objects.transfer import Transfer


class TaxAgencyTests(unittest.TestCase):
    def test_unicode(self):
        transfer = Transfer()
        transfer.Amount = 100

        self.assertEquals(str(transfer), "100")
