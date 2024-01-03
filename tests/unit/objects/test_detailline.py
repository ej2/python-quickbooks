import unittest

from quickbooks.objects.detailline import SalesItemLineDetail, DiscountOverride, DetailLine, SubtotalLineDetail, \
    DiscountLineDetail, SubtotalLine, DescriptionLineDetail, SalesItemLine, DiscountLine, GroupLine, \
    AccountBasedExpenseLineDetail, ItemBasedExpenseLineDetail, DescriptionOnlyLine, ItemBasedExpenseLine


class DetailLineTests(unittest.TestCase):
    def test_unicode(self):
        detail = DetailLine()
        detail.LineNum = 1
        detail.Description = "Product Description"
        detail.Amount = 100

        self.assertEqual(str(detail), "[1] Product Description 100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        sales_detail = SalesItemLineDetail()
        sales_detail.UnitPrice = 10

        self.assertEqual(str(sales_detail), "10")


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_override = DiscountOverride()

        self.assertEqual(discount_override.DiscountPercent, 0)
        self.assertEqual(discount_override.DiscountRef, None)
        self.assertEqual(discount_override.DiscountAccountRef, None)
        self.assertFalse(discount_override.PercentBased)


class DiscountLineDetailTesets(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEqual(discount_detail.Discount, None)
        self.assertEqual(discount_detail.ClassRef, None)
        self.assertEqual(discount_detail.TaxCodeRef, None)

class SubtotalLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEqual(detail.ItemRef, None)


class SubtotalLineTest(unittest.TestCase):
    def test_init(self):
        subtotal_line = SubtotalLine()

        self.assertEqual(subtotal_line.DetailType, "SubTotalLineDetail")
        self.assertEqual(subtotal_line.SubtotalLineDetail, None)


class DescriptionLineDetailTest(unittest.TestCase):
    def test_init(self):
        description_detail = DescriptionLineDetail()

        self.assertEqual(description_detail.ServiceDate, "")
        self.assertEqual(description_detail.TaxCodeRef, None)


class SalesItemLineTest(unittest.TestCase):
    def test_init(self):
        line = SalesItemLine()

        self.assertEqual(line.DetailType, "SalesItemLineDetail")
        self.assertEqual(line.SalesItemLineDetail, None)


class DiscountLineTest(unittest.TestCase):
    def test_init(self):
        line = DiscountLine()

        self.assertEqual(line.DetailType, "DiscountLineDetail")
        self.assertEqual(line.DiscountLineDetail, None)


class GroupLineTest(unittest.TestCase):
    def test_init(self):
        line = GroupLine()

        self.assertEqual(line.DetailType, "GroupLineDetail")
        self.assertEqual(line.GroupLineDetail, None)


class ItemBasedExpenseLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEqual(detail.BillableStatus, None)
        self.assertEqual(detail.UnitPrice, 0)
        self.assertEqual(detail.Qty, 0)
        self.assertEqual(detail.ItemRef, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.PriceLevelRef, None)
        self.assertEqual(detail.TaxCodeRef, None)
        self.assertEqual(detail.MarkupInfo, None)
        self.assertEqual(detail.CustomerRef, None)


class ItemBasedExpenseLineTests(unittest.TestCase):
    def test_unicode(self):
        line = ItemBasedExpenseLine()

        self.assertEqual(line.DetailType, "ItemBasedExpenseLineDetail")
        self.assertEqual(line.ItemBasedExpenseLineDetail, None)


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        acct_detail = AccountBasedExpenseLineDetail()
        acct_detail.BillableStatus = "test"

        self.assertEqual(str(acct_detail), "test")


class DescriptionOnlyLineTests(unittest.TestCase):
    def test_unicode(self):
        line = DescriptionOnlyLine()

        self.assertEqual(line.DetailType, "DescriptionOnly")
        self.assertEqual(line.DescriptionLineDetail, None)
