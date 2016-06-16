import unittest

from quickbooks import QuickBooks
from quickbooks.objects.estimate import Estimate


class EstimateTests(unittest.TestCase):
    def test_unicode(self):
        estimate = Estimate()
        estimate.TotalAmt = 10

        self.assertEquals(str(estimate), "10")

    def test_valid_object_name(self):
        obj = Estimate()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
