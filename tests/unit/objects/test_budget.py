import unittest

from quickbooks.objects.budget import BudgetDetail, Budget


class BudgetDetailTests(unittest.TestCase):
    def test_unicode(self):
        budget_detail = BudgetDetail()
        budget_detail.Amount = 10

        self.assertEquals(str(budget_detail), "10")


class BudgetTests(unittest.TestCase):
    def test_unicode(self):
        budget = Budget()
        budget.Name = "test"

        self.assertEquals(str(budget), "test")
