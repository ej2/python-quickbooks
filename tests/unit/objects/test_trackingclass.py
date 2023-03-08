import unittest

from quickbooks.objects.trackingclass import Class


class ClassTests(unittest.TestCase):
    def test_unicode(self):
        cls = Class()
        cls.Name = "test"

        self.assertEqual(str(cls), "test")

    def test_to_ref(self):
        cls = Class()
        cls.Name = "test"
        cls.Id = 100

        dept_ref = cls.to_ref()

        self.assertEqual(dept_ref.name, "test")
        self.assertEqual(dept_ref.type, "Class")
        self.assertEqual(dept_ref.value, 100)
