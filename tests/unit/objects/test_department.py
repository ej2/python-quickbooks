import unittest

from quickbooks.objects.department import Department


class DepartmentTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        department = Department()
        department.FullyQualifiedName = "test"

        self.assertEquals(department.__unicode__(), "test")
