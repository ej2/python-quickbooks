import unittest

from quickbooks.objects.estimate import Estimate, EstimateLine, SalesItemLineDetail, DiscountOverride, \
    DiscountLineDetail, SubtotalLine, DescriptionLineDetail, DescriptionLine, SaleItemLine, DiscountLine


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


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_override = DiscountOverride()

        self.assertEquals(discount_override.DiscountPercent, 0)
        self.assertEquals(discount_override.DiscountRef, None)
        self.assertEquals(discount_override.DiscountAccountRef, None)
        self.assertFalse(discount_override.PercentBased)


class DiscountLineDetailTesets(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEquals(discount_detail.Discount, None)
        self.assertEquals(discount_detail.ClassRef, None)
        self.assertEquals(discount_detail.TaxCodeRef, None)


class SubtotalLineTest(unittest.TestCase):
    def test_init(self):
        subtotal_line = SubtotalLine()

        self.assertEquals(subtotal_line.DetailType, "SubtotalLineDetail")
        self.assertEquals(subtotal_line.SubtotalLineDetail, None)


class DescriptionLineDetailTest(unittest.TestCase):
    def test_init(self):
        description_detail = DescriptionLineDetail()

        self.assertEquals(description_detail.ServiceDate, "")
        self.assertEquals(description_detail.TaxCodeRef, None)


class DescriptionLineTest(unittest.TestCase):
    def test_init(self):
        line = DescriptionLine()

        self.assertEquals(line.DetailType, "DescriptionOnly")
        self.assertEquals(line.DescriptionLineDetail, None)


class SaleItemLineTest(unittest.TestCase):
    def test_init(self):
        line = SaleItemLine()

        self.assertEquals(line.DetailType, "SalesItemLineDetail")
        self.assertEquals(line.SalesItemLineDetail, None)


class DiscountLineTest(unittest.TestCase):
    def test_init(self):
        line = DiscountLine()

        self.assertEquals(line.DetailType, "DiscountLineDetail")
        self.assertEquals(line.DiscountLineDetail, None)
