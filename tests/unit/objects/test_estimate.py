import unittest

from quickbooks.objects.estimate import Estimate, EstimateLine, SalesItemLineDetail


class EstimateTests(unittest.TestCase):
    def test_unicode(self):
        estimate = Estimate()
        estimate.TotalAmt = 10

        self.assertEquals(estimate.__unicode__(), 10)


class EstimatelineTests(unittest.TestCase):
    def test_unicode(self):
        estimateline = EstimateLine()
        estimateline.Amount = 100

        self.assertEquals(estimateline.__unicode__(), 100)


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        sales_detail = SalesItemLineDetail()
        sales_detail.UnitPrice = 10

        self.assertEquals(sales_detail.__unicode__(), 10)
