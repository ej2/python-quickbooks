from datetime import datetime

from quickbooks.objects.base import CustomerMemo
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from quickbooks.objects.base import EmailAddress
from tests.integration.test_base import QuickbooksTestCase
import uuid


class InvoiceTest(QuickbooksTestCase):
    def create_invoice_line(self):
        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        line.SalesItemLineDetail = SalesItemLineDetail()
        item = Item.all(max_results=1, qb=self.qb_client)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        return line

    def create_invoice(self, customer, request_id=None):
        invoice = Invoice()
        invoice.Line.append(self.create_invoice_line())

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
        self.assertEqual(invoice[0].CustomerRef.name, customer.DisplayName)

    def test_where(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]

        invoice = Invoice.where(
            "CustomerRef = '{0}'".format(customer.Id), qb=self.qb_client)

        print(invoice[0])
        self.assertEqual(invoice[0].CustomerRef.name, customer.DisplayName)

    def test_create(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice = self.create_invoice(customer)
        query_invoice = Invoice.get(invoice.Id, qb=self.qb_client)

        self.assertEqual(query_invoice.CustomerRef.name, customer.DisplayName)
        self.assertEqual(query_invoice.CustomerMemo.value, "Customer Memo")
        self.assertEqual(query_invoice.Line[0].Description, "description")
        self.assertEqual(query_invoice.Line[0].Amount, 100.0)
    
    def test_create_idempotence(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        sample_request_id = str(uuid.uuid4())
        invoice = self.create_invoice(customer, request_id=sample_request_id)
        duplicate_invoice = self.create_invoice(customer, request_id=sample_request_id)

        # Assert that both returned invoices have the same id
        self.assertEqual(invoice.Id, duplicate_invoice.Id)

    def test_delete(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        # First create an invoice
        invoice = self.create_invoice(customer)

        # Then delete
        invoice_id = invoice.Id
        invoice.delete(qb=self.qb_client)

        query_invoice = Invoice.filter(Id=invoice_id, qb=self.qb_client)
        self.assertEqual([], query_invoice)

    def test_void(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        invoice = self.create_invoice(customer)
        invoice_id = invoice.Id
        invoice.void(qb=self.qb_client)

        query_invoice = Invoice.get(invoice_id, qb=self.qb_client)
        self.assertEqual(query_invoice.Balance, 0.0)
        self.assertEqual(query_invoice.TotalAmt, 0.0)
        self.assertIn('Voided', query_invoice.PrivateNote)

    def test_invoice_link(self):
        # Sharable link for the invoice sent to external customers.
        # The link is generated only for invoices with online payment enabled and having a valid customer email address.
        # Include query param `include=invoiceLink` to get the link back on query response.

        # Create test customer
        customer_name = datetime.now().strftime('%d%H%M%S')
        customer = Customer()
        customer.DisplayName = customer_name
        customer.save(qb=self.qb_client)

        # Create an invoice with sharable link flags set
        invoice = Invoice()
        invoice.CustomerRef = customer.to_ref()
        invoice.DueDate = '2024-12-31'
        invoice.AllowOnlineCreditCardPayment = True
        invoice.AllowOnlineACHPayment = True
        invoice.Line.append(self.create_invoice_line())

        # BillEmail must be set for Sharable link to work!
        invoice.BillEmail = EmailAddress()
        invoice.BillEmail.Address = 'test@email.com'

        invoice.save(qb=self.qb_client)

        # You must add 'include': 'invoiceLink' to the params when doing a query for the invoice
        query_invoice = Invoice.get(invoice.Id, qb=self.qb_client, params={'include': 'invoiceLink'})

        self.assertIsNotNone(query_invoice.InvoiceLink)
        self.assertIn('https', query_invoice.InvoiceLink)
