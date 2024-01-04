import unittest

from quickbooks import QuickBooks
from quickbooks.objects.recurringtransaction import RecurringTransaction, ScheduleInfo, RecurringInfo


class RecurringTransactionTests(unittest.TestCase):
    def test_valid_object_name(self):
        obj = RecurringTransaction()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class ScheduleInfoTest(unittest.TestCase):
    def test_create(self):
        obj = ScheduleInfo()
        obj.DayOfMonth = "1"

        self.assertEqual(obj.DayOfMonth, "1")


class RecurringInfoTest(unittest.TestCase):
    def test_create(self):
        obj = RecurringInfo()

        self.assertEqual(obj.RecurType, "Automated")

