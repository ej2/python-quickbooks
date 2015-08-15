import unittest

from quickbooks.objects.employee import Employee


class EmployeeTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        employee = Employee()
        employee.FullyQualifiedName = "test"

        self.assertEquals(employee.__unicode__(), "test")
