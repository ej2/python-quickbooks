import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.helpers import qb_datetime_utc_offset_format
from quickbooks.objects.employee import Employee
from quickbooks.objects.timeactivity import TimeActivity


class TimeActivityTest(unittest.TestCase):
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

        self.name = "Test {0}".format(datetime.now().strftime('%d%H%M'))

    def test_create(self):
        employee = Employee.all(max_results=1, qb=self.qb_client)[0]

        time_activity = TimeActivity()
        time_activity.NameOf = "Employee"

        time_activity.EmployeeRef = employee.to_ref()
        time_activity.Description = "Test description"
        time_activity.StartTime = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 10, 0), '-07:00')
        time_activity.EndTime = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 11, 0), '-07:00')
        time_activity.save(qb=self.qb_client)

        query_time_activity = TimeActivity.get(time_activity.Id, qb=self.qb_client)

        self.assertEquals(query_time_activity.Id, time_activity.Id)
        self.assertEquals(query_time_activity.NameOf, "Employee")
        self.assertEquals(query_time_activity.Description, "Test description")
        self.assertEquals(query_time_activity.EmployeeRef.value, employee.Id)

        # Quickbooks has issues with returning the correct StartTime and EndTime
        #self.assertEquals(query_time_activity.StartTime, '2016-07-22T10:00:00-07:00')
        #self.assertEquals(query_time_activity.EndTime, '2016-07-22T11:00:00-07:00')

    def test_update(self):
        time_activity = TimeActivity.all(max_results=1, qb=self.qb_client)[0]
        time_activity.Description = "Updated test description"
        time_activity.save(qb=self.qb_client)

        query_time_activity = TimeActivity.get(time_activity.Id, qb=self.qb_client)

        self.assertEquals(query_time_activity.Description, "Updated test description")
