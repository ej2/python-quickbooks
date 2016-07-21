import unittest

from quickbooks.objects.base import CustomerMemo, CustomField, Ref, WebAddress, EmailAddress, PhoneNumber, \
    Address, LinkedTxn, MetaData, MarkupInfo, AttachableRef, LinkedTxnMixin

from quickbooks.objects.deposit import Deposit


class AddressTests(unittest.TestCase):
    def test_unicode(self):
        address = Address()
        address.Line1 = "123 Main"
        address.City = "Joplin"
        address.CountrySubDivisionCode = "MO"
        address.PostalCode = "12345"

        self.assertEquals(str(address), "123 Main Joplin, MO 12345")


class PhoneNumberTests(unittest.TestCase):
    def test_unicode(self):
        number = PhoneNumber()
        number.FreeFormNumber = "555-555-5555"

        self.assertEquals(str(number), "555-555-5555")


class EmailAddressTests(unittest.TestCase):
    def test_unicode(self):
        email = EmailAddress()
        email.Address = "email@gmail.com"

        self.assertEquals(str(email), "email@gmail.com")


class WebAddressTests(unittest.TestCase):
    def test_unicode(self):
        url = WebAddress()
        url.URI = "www.website.com"

        self.assertEquals(str(url), "www.website.com")


class RefTests(unittest.TestCase):
    def test_unicode(self):
        ref = Ref()
        ref.type = "type"
        ref.name = "test"
        ref.value = 1

        self.assertEquals(str(ref), "test")


class CustomFieldTests(unittest.TestCase):
    def test_unicode(self):
        custom = CustomField()
        custom.Name = "name"

        self.assertEquals(str(custom), "name")


class CustomerMemoTests(unittest.TestCase):
    def test_unicode(self):
        memo = CustomerMemo()
        memo.value = "value"

        self.assertEquals(str(memo), "value")


class LinkedTxnTests(unittest.TestCase):
    def test_unicode(self):
        linked = LinkedTxn()
        linked.TxnId = 1

        self.assertEquals(str(linked), "1")


class MetaDataTests(unittest.TestCase):
    def test_unicode(self):
        meta = MetaData()
        meta.CreateTime = "1/1/2000"

        self.assertEquals(str(meta), "Created 1/1/2000")


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
        attachable.IncludeOnSend = False
        attachable.Inactive = False
        attachable.NoRefOnly = False

        self.assertEquals(attachable.LineInfo, None)
        self.assertEquals(attachable.IncludeOnSend, False)
        self.assertEquals(attachable.Inactive, False)
        self.assertEquals(attachable.NoRefOnly, False)
        self.assertEquals(attachable.EntityRef, None)


class LinkedTxnMixinTests(unittest.TestCase):
    def test_to_linked_txn(self):

        deposit = Deposit()
        deposit.Id = 100

        linked_txn = deposit.to_linked_txn()

        self.assertEquals(linked_txn.TxnId, 100)
        self.assertEquals(linked_txn.TxnType, "Deposit")
        self.assertEquals(linked_txn.TxnLineId, 1)
