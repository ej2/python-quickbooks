import unittest
from quickbooks import utils


class UtilsTests(unittest.TestCase):
    def test_build_where_clause(self):
        where_clause = utils.build_where_clause(field1=1,
                                                field2="Someone's Company")

        self.assertTrue("field1 = 1" in where_clause)
        self.assertTrue("field2 = 'Someone\\\'s Company'" in where_clause)

    def test_build_where_clause_unicode(self):
        where_clause = utils.build_where_clause(field1=u"Test 1",
                                                field2=u"Someone's Company")

        self.assertTrue("field1 = 'Test 1'" in where_clause)
        self.assertTrue("field2 = 'Someone\\\'s Company'" in where_clause)

    def test_build_where_clause_operators(self):
        where_clause = utils.build_where_clause(field1__gt=10,
                                                field2__gte=12,
                                                field3__lt="it's",
                                                field4__lte='16',
                                                field5__like="mike")

        self.assertTrue("field1 > 10" in where_clause)
        self.assertTrue("field2 >= 12" in where_clause)
        self.assertTrue("field3 < 'it\\\'s'" in where_clause)
        self.assertTrue("field4 <= '16'" in where_clause)
        self.assertTrue("field5 LIKE 'mike'" in where_clause)

    def test_build_where_clause_in(self):
        where_clause = utils.build_where_clause(field1__in=["hakuna", "matata"],
                                                field2__in=[1, 2],
                                                field3__in=["Fred's", "Bill's"])

        self.assertTrue("field1 IN ('hakuna', 'matata')" in where_clause)
        self.assertTrue("field2 IN ('1', '2')" in where_clause)
        self.assertTrue("field3 IN ('Fred\\\'s', 'Bill\\\'s')" in where_clause)

    def test_build_choose_clause_integers(self):
        where_clause = utils.build_choose_clause(choices=[1, 2],
                                                 field="field1")

        self.assertEqual(where_clause, "field1 in (1, 2)")

    def test_build_choose_clause_strings(self):
        where_clause = utils.build_choose_clause(choices=["val1", "val2"],
                                                 field="field1")

        self.assertEqual(where_clause, "field1 in ('val1', 'val2')")

    def test_build_choose_clause_quoted_value(self):
        where_clause = utils.build_choose_clause(choices=["val1",
                                                          "Someone's Company"],
                                                 field="field1")

        self.assertEqual(where_clause, "field1 in ('val1', 'Someone\\\'s Company')")

    def test_build_choose_clause_unicode(self):
        where_clause = utils.build_choose_clause(choices=[u"Test - & % $", u"Another Test"],
                                                 field="field1")

        self.assertEqual(where_clause, "field1 in ('Test - & % $', 'Another Test')")

    def test_build_choose_clause_unicode_escaped(self):
        where_clause = utils.build_choose_clause(choices=[u"Test - & % $", u"Another's Test"],
                                                 field="field1")

        self.assertEqual(where_clause, "field1 in ('Test - & % $', 'Another\\\'s Test')")
