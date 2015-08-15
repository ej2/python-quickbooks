import unittest

from quickbooks.objects.budget import BudgetDetail, Budget


class BudgetDetailTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        budget_detail = BudgetDetail()
        budget_detail.Amount = 10

        self.assertEquals(budget_detail.__unicode__(), 10)


class BudgetTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        budget = Budget()
        budget.Name = "test"

        self.assertEquals(budget.__unicode__(), "test")
