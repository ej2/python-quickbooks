import unittest

from quickbooks import QuickBooks
from quickbooks.objects.attachable import Attachable


class AttachableTests(unittest.TestCase):
    def test_unicode(self):
        attachable = Attachable()
        attachable.FileName = "test"

        self.assertEqual(str(attachable), "test")

    def test_to_ref(self):
        attachable = Attachable()
        attachable.FileName = "test"
        attachable.Id = 12

        ref = attachable.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Attachable")
        self.assertEqual(ref.value, 12)

    def test_valid_object_name(self):
        attachable = Attachable()
        client = QuickBooks()
        result = client.isvalid_object_name(attachable.qbo_object_name)

        self.assertTrue(result)
