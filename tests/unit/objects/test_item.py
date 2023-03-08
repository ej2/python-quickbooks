import unittest

from quickbooks import QuickBooks
from quickbooks.objects.item import Item


class ItemTests(unittest.TestCase):
    def test_unicode(self):
        item = Item()
        item.Name = "test"

        self.assertEqual(str(item), "test")

    def test_to_ref(self):
        item = Item()
        item.Name = "test"
        item.Id = 100

        ref = item.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Item")
        self.assertEqual(ref.value, 100)

    def test_valid_object_name(self):
        obj = Item()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
