import unittest

from quickbooks import QuickBooks
from quickbooks.objects import Ref
from quickbooks.objects.invoice import Invoice, DeliveryInfo


class InvoiceTests(unittest.TestCase):
    def test_unicode(self):
        invoice = Invoice()
        invoice.TotalAmt = 10

        self.assertEquals(str(invoice), "10")

    def test_to_LinkedTxn(self):
        invoice = Invoice()
        invoice.TotalAmt = 10
        invoice.Id = 1

        linked_txn = invoice.to_linked_txn()

        self.assertEquals(linked_txn.TxnId, invoice.Id)
        self.assertEquals(linked_txn.TxnType, "Invoice")
        self.assertEquals(linked_txn.TxnLineId, 1)

    def test_email_sent_true(self):
        invoice = Invoice()
        invoice.EmailStatus = "EmailSent"
        self.assertTrue(invoice.email_sent)

    def test_email_sent_false(self):
        invoice = Invoice()
        invoice.EmailStatus = "NotSent"
        self.assertFalse(invoice.email_sent)

    def test_valid_object_name(self):
        obj = Invoice()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        invoice = Invoice()
        invoice.DocNumber = 1
        invoice.Id = 2

        ref = invoice.to_ref()
        self.assertIsInstance(ref, Ref)
        self.assertEquals(ref.type, "Invoice")
        self.assertEquals(ref.name, 1)  # should be DocNumber
        self.assertEquals(ref.value, 2)  # should be Id


class DeliveryInfoTests(unittest.TestCase):
    def test_init(self):
        info = DeliveryInfo()

        self.assertEquals(info.DeliveryType, "")
        self.assertEquals(info.DeliveryTime, "")
