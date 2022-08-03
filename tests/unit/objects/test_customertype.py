import unittest

from quickbooks import QuickBooks
from quickbooks.objects.customertype import CustomerType


class CustomerTypeTests(unittest.TestCase):
    def test_unicode(self):
        customer_type = CustomerType()
        customer_type.Name = "test"

        self.assertEquals(str(customer_type), "test")

    def test_valid_object_name(self):
        obj = CustomerType()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
