import unittest

from quickbooks.objects.invoice import Invoice, InvoiceDetail, SalesItemLineDetail, DiscountLineDetail


class InvoiceTests(unittest.TestCase):
    def test_unicode(self):
        invoice = Invoice()
        invoice.TotalAmt = 10

        self.assertEquals(unicode(invoice), "10")

    def test_to_LinkedTxn(self):
        invoice = Invoice()
        invoice.TotalAmt = 10
        invoice.Id = 1

        linked_txn = invoice.to_linked_txn()

        self.assertEquals(linked_txn.TxnId, invoice.Id)
        self.assertEquals(linked_txn.TxnType, "Invoice")
        self.assertEquals(linked_txn.TxnLineId, 1)


class InvoiceDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = InvoiceDetail()
        detail.LineNum = 1
        detail.Description = "Product Description"
        detail.Amount = 100

        self.assertEquals(unicode(detail), "[1] Product Description 100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 100

        self.assertEquals(unicode(detail), "100")


class DiscountLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = DiscountLineDetail()
        detail.DiscountPercent = 5

        self.assertEquals(unicode(detail), "5")
