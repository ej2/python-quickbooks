import unittest
from mock import patch

from quickbooks.objects.base import PhoneNumber
from quickbooks.objects.department import Department


class ToJsonMixinTest(unittest.TestCase):
    def test_to_json(self):
        phone = PhoneNumber()
        phone.FreeFormNumber = "555-555-5555"

        json = phone.to_json()

        self.assertEquals(json, '{\n    "FreeFormNumber": "555-555-5555"\n}')

