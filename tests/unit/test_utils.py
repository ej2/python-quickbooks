import unittest
from quickbooks import utils


class UtilsTests(unittest.TestCase):
    def setup(self):
        pass

    def test_build_where_clause(self):
        where_clause = utils.build_where_clause(field1=1, field2="value2")

        self.assertTrue(where_clause, "WHERE field1 = 1 AND field2 = 'value2")