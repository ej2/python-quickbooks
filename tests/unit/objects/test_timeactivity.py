import unittest

from quickbooks import QuickBooks
from quickbooks.objects.timeactivity import TimeActivity


class TimeActivityTests(unittest.TestCase):
    def test_unicode(self):
        time_activity = TimeActivity()

        time_activity.NameOf = "test"
        time_activity.TimeZone = "CST"
        time_activity.BillableStatus = "test"
        time_activity.Taxable = False
        time_activity.HourlyRate = 0
        time_activity.Hours = 1
        time_activity.Minutes = 60
        time_activity.BreakHours = 1
        time_activity.BreakMinutes = 60
        time_activity.Description = "test"

        self.assertEquals(str(time_activity), "test")
        self.assertEquals(time_activity.TimeZone, "CST")
        self.assertEquals(time_activity.BillableStatus, "test")
        self.assertEquals(time_activity.Taxable, False)
        self.assertEquals(time_activity.HourlyRate, 0)
        self.assertEquals(time_activity.Hours, 1)
        self.assertEquals(time_activity.Minutes, 60)
        self.assertEquals(time_activity.BreakHours, 1)
        self.assertEquals(time_activity.BreakMinutes, 60)
        self.assertEquals(time_activity.Description, "test")

    def test_valid_object_name(self):
        obj = TimeActivity()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
