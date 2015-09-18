import unittest

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


class DeliveryInfoTests(unittest.TestCase):
    def test_init(self):
        info = DeliveryInfo()

        self.assertEquals(info.DeliveryType, "")
        self.assertEquals(info.DeliveryTime, "")
