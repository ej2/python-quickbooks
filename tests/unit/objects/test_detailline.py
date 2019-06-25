import unittest

from quickbooks.objects.detailline import SalesItemLineDetail, DiscountOverride, DetailLine, SubtotalLineDetail, \
    DiscountLineDetail, SubtotalLine, DescriptionLineDetail, DescriptionLine, SalesItemLine, DiscountLine, GroupLine, \
    AccountBasedExpenseLineDetail, ItemBasedExpenseLineDetail, DescriptionOnlyLine, ItemBasedExpenseLine


class DetailLineTests(unittest.TestCase):
    def test_unicode(self):
        detail = DetailLine()
        detail.LineNum = 1
        detail.Description = "Product Description"
        detail.Amount = 100

        self.assertEquals(str(detail), "[1] Product Description 100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        sales_detail = SalesItemLineDetail()
        sales_detail.UnitPrice = 10

        self.assertEquals(str(sales_detail), "10")


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

class SubtotalLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEquals(detail.ItemRef, None)


class SubtotalLineTest(unittest.TestCase):
    def test_init(self):
        subtotal_line = SubtotalLine()

        self.assertEquals(subtotal_line.DetailType, "SubTotalLineDetail")
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


class SalesItemLineTest(unittest.TestCase):
    def test_init(self):
        line = SalesItemLine()

        self.assertEquals(line.DetailType, "SalesItemLineDetail")
        self.assertEquals(line.SalesItemLineDetail, None)


class DiscountLineTest(unittest.TestCase):
    def test_init(self):
        line = DiscountLine()

        self.assertEquals(line.DetailType, "DiscountLineDetail")
        self.assertEquals(line.DiscountLineDetail, None)


class GroupLineTest(unittest.TestCase):
    def test_init(self):
        line = GroupLine()

        self.assertEquals(line.DetailType, "GroupLineDetail")
        self.assertEquals(line.GroupLineDetail, None)


class ItemBasedExpenseLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEquals(detail.BillableStatus, None)
        self.assertEquals(detail.UnitPrice, 0)
        self.assertEquals(detail.TaxInclusiveAmt, 0)
        self.assertEquals(detail.Qty, 0)
        self.assertEquals(detail.ItemRef, None)
        self.assertEquals(detail.ClassRef, None)
        self.assertEquals(detail.PriceLevelRef, None)
        self.assertEquals(detail.TaxCodeRef, None)
        self.assertEquals(detail.MarkupInfo, None)
        self.assertEquals(detail.CustomerRef, None)


class ItemBasedExpenseLineTests(unittest.TestCase):
    def test_unicode(self):
        line = ItemBasedExpenseLine()

        self.assertEquals(line.DetailType, "ItemBasedExpenseLineDetail")
        self.assertEquals(line.ItemBasedExpenseLineDetail, None)


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        acct_detail = AccountBasedExpenseLineDetail()
        acct_detail.BillableStatus = "test"

        self.assertEquals(str(acct_detail), "test")


class DescriptionOnlyLineTests(unittest.TestCase):
    def test_unicode(self):
        line = DescriptionOnlyLine()

        self.assertEquals(line.DetailType, "DescriptionOnly")
        self.assertEquals(line.DescriptionLineDetail, None)
