import unittest

from quickbooks import QuickBooks
from quickbooks.objects.item import Item


class ItemTests(unittest.TestCase):
    def test_unicode(self):
        item = Item()
        item.Name = "test"

        self.assertEquals(str(item), "test")

    def test_to_ref(self):
        item = Item()
        item.Name = "test"
        item.Id = 100

        ref = item.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Item")
        self.assertEquals(ref.value, 100)

    def test_valid_object_name(self):
        obj = Item()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
