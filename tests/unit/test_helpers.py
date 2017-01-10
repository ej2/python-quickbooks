import unittest

from quickbooks.helpers import qb_date_format, qb_datetime_format, qb_datetime_utc_offset_format
from datetime import datetime, date


class HelpersTests(unittest.TestCase):
    def test_qb_date_format(self):
        result = qb_date_format(date(2016, 7, 22))
        self.assertEquals(result, '2016-07-22')

    def test_qb_datetime_format(self):
        result = qb_datetime_format(datetime(2016, 7, 22, 10, 35, 00))
        self.assertEquals(result, '2016-07-22T10:35:00')

    def test_qb_datetime_utc_offset_format(self):
        result = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 10, 35, 00), '-06:00')
        self.assertEquals(result, '2016-07-22T10:35:00-06:00')
