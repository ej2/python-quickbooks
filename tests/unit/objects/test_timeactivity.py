import unittest

from quickbooks import QuickBooks
from quickbooks.objects.timeactivity import TimeActivity


class TimeActivityTests(unittest.TestCase):
    def test_unicode(self):
        time_activity = TimeActivity()

        time_activity.NameOf = "test"
        time_activity.BillableStatus = "test"
        time_activity.Taxable = False
        time_activity.HourlyRate = 0
        time_activity.Hours = 1
        time_activity.Minutes = 60
        time_activity.BreakHours = 1
        time_activity.BreakMinutes = 60
        time_activity.Description = "test"
        time_activity.CostRate = 50.0

        self.assertEqual(str(time_activity), "test")
        self.assertEqual(time_activity.BillableStatus, "test")
        self.assertEqual(time_activity.Taxable, False)
        self.assertEqual(time_activity.HourlyRate, 0)
        self.assertEqual(time_activity.Hours, 1)
        self.assertEqual(time_activity.Minutes, 60)
        self.assertEqual(time_activity.BreakHours, 1)
        self.assertEqual(time_activity.BreakMinutes, 60)
        self.assertEqual(time_activity.Description, "test")
        self.assertEqual(time_activity.CostRate, 50.0)

    def test_valid_object_name(self):
        obj = TimeActivity()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
