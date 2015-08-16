import unittest

from quickbooks.objects.invoice import Invoice, InvoiceDetail, SalesItemLineDetail, DiscountLineDetail


class InvoiceTests(unittest.TestCase):
    def test_unicode(self):
        invoice = Invoice()
        invoice.TotalAmt = 10

        self.assertEquals(invoice.__unicode__(), 10)


class InvoiceDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = InvoiceDetail()
        detail.LineNum = 1
        detail.Description = "Product Description"
        detail.Amount = 100

        self.assertEquals(detail.__unicode__(), "[1] Product Description 100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 100

        self.assertEquals(detail.__unicode__(), 100)


class DiscountLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = DiscountLineDetail()
        detail.DiscountPercent = 5

        self.assertEquals(detail.__unicode__(), 5)
