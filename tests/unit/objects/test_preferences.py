import unittest

from quickbooks import QuickBooks
from quickbooks.objects.preferences import Preferences


class PreferencesTests(unittest.TestCase):
    def test_unicode(self):
        preferences = Preferences()
        preferences.Id = 137

        self.assertEquals(str(preferences), "Preferences 137")

    def test_valid_object_name(self):
        preferences = Preferences()
        client = QuickBooks()
        result = client.isvalid_object_name(preferences.qbo_object_name)

        self.assertTrue(result)
