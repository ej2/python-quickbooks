import unittest

from quickbooks.objects.base import CustomerMemo, CustomField, Ref, WebAddress, EmailAddress, PhoneNumber, Address, LinkedTxn, MetaData



class AddressTests(unittest.TestCase):
    def test_unicode(self):
        address = Address()
        address.Line1 = "123 Main"
        address.City = "Joplin"
        address.CountrySubDivisionCode = "MO"
        address.PostalCode = "12345"

        self.assertEquals(address.__unicode__(), "123 Main Joplin, MO 12345")


class PhoneNumberTests(unittest.TestCase):
    def test_unicode(self):
        number = PhoneNumber()
        number.FreeFormNumber = "555-555-5555"

        self.assertEquals(number.__unicode__(), "555-555-5555")


class EmailAddressTests(unittest.TestCase):
    def test_unicode(self):
        email = EmailAddress()
        email.Address = "email@gmail.com"

        self.assertEquals(email.__unicode__(), "email@gmail.com")


class WebAddressTests(unittest.TestCase):
    def test_unicode(self):
        url = WebAddress()
        url.URI = "www.website.com"

        self.assertEquals(url.__unicode__(), "www.website.com")


class RefTests(unittest.TestCase):
    def test_unicode(self):
        ref = Ref()
        ref.type = "type"
        ref.name = "test"
        ref.value = 1

        self.assertEquals(ref.__unicode__(), "test")


class CustomFieldTests(unittest.TestCase):
    def test_unicode(self):
        custom = CustomField()
        custom.Name = "name"

        self.assertEquals(custom.__unicode__(), "name")


class CustomerMemoTests(unittest.TestCase):
    def test_unicode(self):
        memo = CustomerMemo()
        memo.Value = "value"

        self.assertEquals(memo.__unicode__(), "value")


class LinkedTxnTests(unittest.TestCase):
    def test_unicode(self):
        linked = LinkedTxn()
        linked.TxnId = 1

        self.assertEquals(linked.__unicode__(), 1)


class MetaDataTests(unittest.TestCase):
    def test_unicode(self):
        meta = MetaData()
        meta.CreateTime = "1/1/2000"

        self.assertEquals(meta.__unicode__(), "Created 1/1/2000")

