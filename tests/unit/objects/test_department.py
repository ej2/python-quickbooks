import unittest

from quickbooks import QuickBooks
from quickbooks.objects.department import Department


class DepartmentTests(unittest.TestCase):
    def test_unicode(self):
        department = Department()
        department.Name = "test"

        self.assertEqual(str(department), "test")

    def test_to_ref(self):
        department = Department()
        department.Name = "test"
        department.Id = 100

        dept_ref = department.to_ref()

        self.assertEqual(dept_ref.name, "test")
        self.assertEqual(dept_ref.type, "Department")
        self.assertEqual(dept_ref.value, 100)

    def test_valid_object_name(self):
        obj = Department()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
