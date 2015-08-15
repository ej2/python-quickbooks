import unittest

from quickbooks.objects.customer import Customer


class BatchTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        customer = Customer()
        customer.DisplayName = "test"

        self.assertEquals(customer.__unicode__(), "test")

    def test_to_ref(self):
        customer = Customer()
        customer.DisplayName = "test"
        customer.Id  = 100

        ref = customer.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Customer")
        self.assertEquals(ref.value, 100)
