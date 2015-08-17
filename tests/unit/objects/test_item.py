import unittest

from quickbooks.objects.item import Item


class ItemTests(unittest.TestCase):
    def test_unicode(self):
        item = Item()
        item.Name = "test"

        self.assertEquals(unicode(item), "test")
