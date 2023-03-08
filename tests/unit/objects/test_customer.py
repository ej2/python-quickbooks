import unittest

from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer


class CustomerTests(unittest.TestCase):
    def test_unicode(self):
        customer = Customer()
        customer.DisplayName = "test"

        self.assertEqual(str(customer), "test")

    def test_to_ref(self):
        customer = Customer()
        customer.DisplayName = "test"
        customer.Id = 100

        ref = customer.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Customer")
        self.assertEqual(ref.value, 100)

    def test_valid_object_name(self):
        obj = Customer()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)
