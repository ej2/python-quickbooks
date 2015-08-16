import unittest

from quickbooks.objects.item import Item


class ItemTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        item = Item()
        item.Name = "test"

        self.assertEquals(item.__unicode__(), "test")
