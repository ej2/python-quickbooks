import unittest

from quickbooks.objects.term import Term


class TermTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Term()
        deposit.Name = "test"

        self.assertEquals(unicode(deposit), "test")
