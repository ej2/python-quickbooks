import unittest

from quickbooks.objects.department import Department


class DepartmentTests(unittest.TestCase):
    def test_unicode(self):
        department = Department()
        department.FullyQualifiedName = "test"

        self.assertEquals(unicode(department), "test")
