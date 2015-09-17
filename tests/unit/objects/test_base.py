import unittest

from quickbooks.objects.base import CustomerMemo, CustomField, Ref, WebAddress, EmailAddress, PhoneNumber, \
    Address, LinkedTxn, MetaData, MarkupInfo, AttachableRef


class AddressTests(unittest.TestCase):
    def test_unicode(self):
        address = Address()
        address.Line1 = "123 Main"
        address.City = "Joplin"
        address.CountrySubDivisionCode = "MO"
        address.PostalCode = "12345"

        self.assertEquals(unicode(address), "123 Main Joplin, MO 12345")


class PhoneNumberTests(unittest.TestCase):
    def test_unicode(self):
        number = PhoneNumber()
        number.FreeFormNumber = "555-555-5555"

        self.assertEquals(unicode(number), "555-555-5555")


class EmailAddressTests(unittest.TestCase):
    def test_unicode(self):
        email = EmailAddress()
        email.Address = "email@gmail.com"

        self.assertEquals(unicode(email), "email@gmail.com")


class WebAddressTests(unittest.TestCase):
    def test_unicode(self):
        url = WebAddress()
        url.URI = "www.website.com"

        self.assertEquals(unicode(url), "www.website.com")


class RefTests(unittest.TestCase):
    def test_unicode(self):
        ref = Ref()
        ref.type = "type"
        ref.name = "test"
        ref.value = 1

        self.assertEquals(unicode(ref), "test")


class CustomFieldTests(unittest.TestCase):
    def test_unicode(self):
        custom = CustomField()
        custom.Name = "name"

        self.assertEquals(unicode(custom), "name")


class CustomerMemoTests(unittest.TestCase):
    def test_unicode(self):
        memo = CustomerMemo()
        memo.Value = "value"

        self.assertEquals(unicode(memo), "value")


class LinkedTxnTests(unittest.TestCase):
    def test_unicode(self):
        linked = LinkedTxn()
        linked.TxnId = 1

        self.assertEquals(unicode(linked), "1")


class MetaDataTests(unittest.TestCase):
    def test_unicode(self):
        meta = MetaData()
        meta.CreateTime = "1/1/2000"

        self.assertEquals(unicode(meta), "Created 1/1/2000")


class MarkupInfoTests(unittest.TestCase):
    def test_init(self):
        markup = MarkupInfo()

        self.assertEquals(markup.PercentBased, False)
        self.assertEquals(markup.Value, 0)
        self.assertEquals(markup.Percent, 0)
        self.assertEquals(markup.PriceLevelRef, None)


class AttachableRefTests(unittest.TestCase):
    def test_init(self):
        attachable = AttachableRef()
        attachable.Name = "test"

        self.assertEquals(attachable.LineInfo, "")
        self.assertEquals(attachable.IncludeOnSend, False)
        self.assertEquals(attachable.Inactive, False)
        self.assertEquals(attachable.NoRefOnly, False)
        self.assertEquals(attachable.EntityRef, None)