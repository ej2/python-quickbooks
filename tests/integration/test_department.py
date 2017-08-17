import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.objects.department import Department

from quickbooks import QuickBooks


class DepartmentTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
        )

        self.qb_client = QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id=os.environ.get('COMPANY_ID')
        )

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
