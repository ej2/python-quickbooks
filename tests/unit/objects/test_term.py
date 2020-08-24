import unittest

from quickbooks import QuickBooks
from quickbooks.objects.term import Term


class TermTests(unittest.TestCase):
    def test_unicode(self):
        term = Term()
        term.Name = "test"

        self.assertEquals(str(term), "test")

    def test_valid_object_name(self):
        obj = Term()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        term = Term()
        term.Name = "test"
        term.Id = 100

        ref = term.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Term")
        self.assertEquals(ref.value, 100)
