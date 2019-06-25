from quickbooks.objects.base import CustomerMemo
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from tests.integration.test_base import QuickbooksTestCase


class InvoiceTest(QuickbooksTestCase):
    def test_create(self):
        invoice = Invoice()

        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        line.SalesItemLineDetail = SalesItemLineDetail()
        item = Item.all(max_results=1, qb=self.qb_client)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        invoice.Line.append(line)

        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice.CustomerRef = customer.to_ref()

        invoice.CustomerMemo = CustomerMemo()
        invoice.CustomerMemo.value = "Customer Memo"
        invoice.save(qb=self.qb_client)

        query_invoice = Invoice.get(invoice.Id, qb=self.qb_client)

        self.assertEquals(query_invoice.CustomerRef.name, customer.DisplayName)
        self.assertEquals(query_invoice.CustomerMemo.value, "Customer Memo")
        self.assertEquals(query_invoice.Line[0].Description, "description")
        self.assertEquals(query_invoice.Line[0].Amount, 100.0)

    def test_delete(self):
        # First create an invoice
        invoice = Invoice()

        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        line.SalesItemLineDetail = SalesItemLineDetail()
        item = Item.all(max_results=1, qb=self.qb_client)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        invoice.Line.append(line)

        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice.CustomerRef = customer.to_ref()

        invoice.CustomerMemo = CustomerMemo()
        invoice.CustomerMemo.value = "Customer Memo"
        invoice.save(qb=self.qb_client)

        # Then delete
        invoice_id = invoice.Id
        invoice.delete(qb=self.qb_client)

        query_invoice = Invoice.filter(Id=invoice_id, qb=self.qb_client)
        self.assertEqual([], query_invoice)
