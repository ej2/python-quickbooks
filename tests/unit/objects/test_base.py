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

        self.assertEqual(str(address), "123 Main Joplin, MO 12345")


class PhoneNumberTests(unittest.TestCase):
    def test_unicode(self):
        number = PhoneNumber()
        number.FreeFormNumber = "555-555-5555"

        self.assertEqual(str(number), "555-555-5555")


class EmailAddressTests(unittest.TestCase):
    def test_unicode(self):
        email = EmailAddress()
        email.Address = "email@gmail.com"

        self.assertEqual(str(email), "email@gmail.com")


class WebAddressTests(unittest.TestCase):
    def test_unicode(self):
        url = WebAddress()
        url.URI = "www.website.com"

        self.assertEqual(str(url), "www.website.com")


class RefTests(unittest.TestCase):
    def test_unicode(self):
        ref = Ref()
        ref.type = "type"
        ref.name = "test"
        ref.value = 1

        self.assertEqual(str(ref), "test")


class CustomFieldTests(unittest.TestCase):
    def test_unicode(self):
        custom = CustomField()
        custom.Name = "name"

        self.assertEqual(str(custom), "name")


class CustomerMemoTests(unittest.TestCase):
    def test_unicode(self):
        memo = CustomerMemo()
        memo.value = "value"

        self.assertEqual(str(memo), "value")


class LinkedTxnTests(unittest.TestCase):
    def test_unicode(self):
        linked = LinkedTxn()
        linked.TxnId = 1

        self.assertEqual(str(linked), "1")


class MetaDataTests(unittest.TestCase):
    def test_unicode(self):
        meta = MetaData()
        meta.CreateTime = "1/1/2000"

        self.assertEqual(str(meta), "Created 1/1/2000")


class MarkupInfoTests(unittest.TestCase):
    def test_init(self):
        markup = MarkupInfo()

        self.assertEqual(markup.PercentBased, False)
        self.assertEqual(markup.Value, 0)
        self.assertEqual(markup.Percent, 0)
        self.assertEqual(markup.PriceLevelRef, None)


class AttachableRefTests(unittest.TestCase):
    def test_init(self):
        attachable = AttachableRef()
        attachable.Name = "test"
        attachable.IncludeOnSend = False
        attachable.Inactive = False
        attachable.NoRefOnly = False

        self.assertEqual(attachable.LineInfo, None)
        self.assertEqual(attachable.IncludeOnSend, False)
        self.assertEqual(attachable.Inactive, False)
        self.assertEqual(attachable.NoRefOnly, False)
        self.assertEqual(attachable.EntityRef, None)


class LinkedTxnMixinTests(unittest.TestCase):
    def test_to_linked_txn(self):

        deposit = Deposit()
        deposit.Id = 100

        linked_txn = deposit.to_linked_txn()

        self.assertEqual(linked_txn.TxnId, 100)
        self.assertEqual(linked_txn.TxnType, "Deposit")
        self.assertEqual(linked_txn.TxnLineId, 1)
