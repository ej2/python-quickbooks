import unittest
from quickbooks import utils


class UtilsTests(unittest.TestCase):
    def test_build_where_clause(self):
        where_clause = utils.build_where_clause(field1=1, field2="Someone's Company")

        self.assertTrue("field1 = 1" in where_clause)
        self.assertTrue("field2 = 'Someone\\\'s Company'" in where_clause)

    def test_build_where_clause_integers(self):
        where_clause = utils.build_choose_clause(choices=[1, 2], field="field1")

        self.assertEqual(where_clause, "field1 in (1, 2)")

    def test_build_where_clause_strings(self):
        where_clause = utils.build_choose_clause(choices=["val1", "val2"], field="field1")

        self.assertEqual(where_clause, "field1 in ('val1', 'val2')")

    def test_build_where_clause_quoted_value(self):
        where_clause = utils.build_choose_clause(choices=["val1", "Someone's Company"], field="field1")

        self.assertEqual(where_clause, "field1 in ('val1', 'Someone\\\'s Company')")
