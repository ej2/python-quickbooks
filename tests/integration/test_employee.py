from datetime import datetime

from quickbooks.objects.base import Address, PhoneNumber
from quickbooks.objects.employee import Employee
from tests.integration.test_base import QuickbooksTestCase


class EmployeeTest(QuickbooksTestCase):
    def test_create(self):
        employee = Employee()
        employee.SSN = "444-55-6666"
        employee.GivenName = "John"
        employee.FamilyName = "Smith {0}".format(datetime.now().strftime('%d%H%M%S'))

        employee.PrimaryAddr = Address()
        employee.PrimaryAddr.Line1 = "45 N. Elm Street"
        employee.PrimaryAddr.City = "Middlefield"
        employee.PrimaryAddr.CountrySubDivisionCode = "CA"
        employee.PrimaryAddr.PostalCode = "93242"

        employee.PrimaryPhone = PhoneNumber()
        employee.PrimaryPhone.FreeFormNumber = "408-525-1234"
        employee.save(qb=self.qb_client)

        query_employee = Employee.get(employee.Id, qb=self.qb_client)

        self.assertEqual(query_employee.Id, employee.Id)
        self.assertEqual(query_employee.SSN, "XXX-XX-XXXX")
        self.assertEqual(query_employee.GivenName, employee.GivenName)
        self.assertEqual(query_employee.FamilyName, employee.FamilyName)
        self.assertEqual(query_employee.PrimaryAddr.Line1, employee.PrimaryAddr.Line1)
        self.assertEqual(query_employee.PrimaryAddr.City, employee.PrimaryAddr.City)
        self.assertEqual(query_employee.PrimaryAddr.CountrySubDivisionCode, employee.PrimaryAddr.CountrySubDivisionCode)
        self.assertEqual(query_employee.PrimaryAddr.PostalCode, employee.PrimaryAddr.PostalCode)
        self.assertEqual(query_employee.PrimaryPhone.FreeFormNumber, employee.PrimaryPhone.FreeFormNumber)

    def test_update(self):
        employee = Employee.all(max_results=1, qb=self.qb_client)[0]
        unique_name = employee.FamilyName = "Smith Updated {0}".format(datetime.now().strftime('%d%H%M%S'))

        employee.FamilyName = unique_name
        employee.save(qb=self.qb_client)

        query_employee = Employee.get(employee.Id, qb=self.qb_client)

        self.assertEqual(query_employee.FamilyName, unique_name)
