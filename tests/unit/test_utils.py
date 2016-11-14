import unittest
from quickbooks import utils


class UtilsTests(unittest.TestCase):
    def setup(self):
        pass

    def test_build_where_clause(self):
        where_clause = utils.build_where_clause(field1=1, field2="value2")

        self.assertTrue(where_clause, "WHERE field1 = 1 AND field2 = 'value2")

    def test_build_where_clause_quote_strings(self):
        where_clause = utils.build_where_clause(field1="value2's")

        self.assertEqual(where_clause, "field1 = 'value2\\'s'")

    def test_build_where_clause_integers(self):
        where_clause = utils.build_choose_clause(choices=[1, 2], field="field1")

        self.assertTrue(where_clause, "WHERE field1 in (1, 2)")

    def test_build_where_clause_strings(self):
        where_clause = utils.build_choose_clause(choices=["val1", "val2"], field="field1")

        self.assertTrue(where_clause, "WHERE field1 in ('val1', 'val2')")

    def test_build_choose_clause_quote_strings(self):
        where_clause = utils.build_choose_clause(choices=["val1's"], field="field1")

        self.assertEqual(where_clause, "field1 in ('val1\\'s')")
