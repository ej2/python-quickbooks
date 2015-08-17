import unittest

from quickbooks.objects.employee import Employee


class EmployeeTests(unittest.TestCase):
    def test_unicode(self):
        employee = Employee()
        employee.DisplayName = "test"

        self.assertEquals(unicode(employee), "test")
