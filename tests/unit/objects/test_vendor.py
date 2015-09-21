import unittest

from quickbooks.objects.vendor import Vendor, ContactInfo


class VendorTests(unittest.TestCase):
    def test_unicode(self):
        vendor = Vendor()
        vendor.DisplayName = "test"

        self.assertEquals(str(vendor), "test")

    def test_to_ref(self):
        vendor = Vendor()
        vendor.DisplayName = "test"
        vendor.Id = 100

        ref = vendor.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Vendor")
        self.assertEquals(ref.value, 100)


class ContactInfoTests(unittest.TestCase):
    def test_init(self):
        contact_info = ContactInfo()

        self.assertEquals(contact_info.Type, "")
        self.assertEquals(contact_info.Telephone, None)
