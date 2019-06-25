from datetime import datetime

from quickbooks.objects.department import Department
from tests.integration.test_base import QuickbooksTestCase


class DepartmentTest(QuickbooksTestCase):
    def setUp(self):
        super(DepartmentTest, self).setUp()

        self.name = "Test Department {0}".format(datetime.now().strftime('%d%H%M%S'))

    def test_create(self):
        department = Department()
        department.Name = self.name
        department.save(qb=self.qb_client)

        query_department = Department.get(department.Id, qb=self.qb_client)

        self.assertEqual(department.Id, query_department.Id)
        self.assertEqual(query_department.Name, self.name)

    def test_update(self):
        department = Department.all(max_results=1, qb=self.qb_client)[0]
        unique_name = "Test Department {0}".format(datetime.now().strftime('%d%H%M%S'))

        department.Name = unique_name
        department.save(qb=self.qb_client)

        query_department = Department.get(department.Id, qb=self.qb_client)

        self.assertEqual(query_department.Name, unique_name)
