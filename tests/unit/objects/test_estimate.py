import unittest

from quickbooks.objects.estimate import Estimate, EstimateLine, SalesItemLineDetail


class EstimateTests(unittest.TestCase):
    def test_unicode(self):
        estimate = Estimate()
        estimate.TotalAmt = 10

        self.assertEquals(unicode(estimate), "10")


class EstimatelineTests(unittest.TestCase):
    def test_unicode(self):
        estimateline = EstimateLine()
        estimateline.Amount = 100

        self.assertEquals(unicode(estimateline), "100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        sales_detail = SalesItemLineDetail()
        sales_detail.UnitPrice = 10

        self.assertEquals(unicode(sales_detail), "10")
