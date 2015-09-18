import unittest

from quickbooks.objects.term import Term


class TermTests(unittest.TestCase):
    def test_unicode(self):
        term = Term()
        term.Name = "test"

        self.assertEquals(str(term), "test")


