from quickbooks.objects.base import CustomerMemo
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from tests.integration.test_base import QuickbooksTestCase
import uuid

class InvoiceTest(QuickbooksTestCase):
    def create_invoice(self, customer, request_id=None):
        invoice = Invoice()

        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        line.SalesItemLineDetail = SalesItemLineDetail()
        item = Item.all(max_results=1, qb=self.qb_client)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        invoice.Line.append(line)

        invoice.CustomerRef = customer.to_ref()

        invoice.CustomerMemo = CustomerMemo()
        invoice.CustomerMemo.value = "Customer Memo"
        invoice.save(qb=self.qb_client, request_id=request_id)
        return invoice
      
    def test_query_by_customer_ref(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice = Invoice.query(
            "select * from Invoice where CustomerRef = '{0}'".format(customer.Id), qb=self.qb_client)

        print(invoice[0].Line[0].LineNum)
        print(invoice[0].Line[0].Amount)
        self.assertEquals(invoice[0].CustomerRef.name, customer.DisplayName)

    def test_where(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]

        invoice = Invoice.where(
            "CustomerRef = '{0}'".format(customer.Id), qb=self.qb_client)

        print(invoice[0])
        self.assertEquals(invoice[0].CustomerRef.name, customer.DisplayName)

    def test_create(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice = self.create_invoice(customer)
        query_invoice = Invoice.get(invoice.Id, qb=self.qb_client)

        self.assertEquals(query_invoice.CustomerRef.name, customer.DisplayName)
        self.assertEquals(query_invoice.CustomerMemo.value, "Customer Memo")
        self.assertEquals(query_invoice.Line[0].Description, "description")
        self.assertEquals(query_invoice.Line[0].Amount, 100.0)
    
    def test_create_idempotence(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        sample_request_id = str(uuid.uuid4())
        invoice = self.create_invoice(customer, request_id=sample_request_id)
        duplicate_invoice = self.create_invoice(customer, request_id=sample_request_id)

        # Assert that both returned invoices have the same id
        self.assertEquals(invoice.Id, duplicate_invoice.Id)

    def test_delete(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        # First create an invoice
        invoice = self.create_invoice(customer)

        # Then delete
        invoice_id = invoice.Id
        invoice.delete(qb=self.qb_client)

        query_invoice = Invoice.filter(Id=invoice_id, qb=self.qb_client)
        self.assertEqual([], query_invoice)
