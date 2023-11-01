from datetime import datetime

from quickbooks.objects import SalesReceipt, Customer, \
    SalesItemLine, SalesItemLineDetail, Item
from tests.integration.test_base import QuickbooksTestCase


class SalesReceiptTest(QuickbooksTestCase):
    def setUp(self):
        super(SalesReceiptTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def create_sales_receipt(self, qty=1, unit_price=100.0):
        sales_receipt = SalesReceipt()
        sales_receipt.TotalAmt = qty * unit_price
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        sales_receipt.CustomerRef = customer.to_ref()
        item = Item.all(max_results=1, qb=self.qb_client)[0]
        line = SalesItemLine()
        sales_item_line_detail = SalesItemLineDetail()
        sales_item_line_detail.ItemRef = item.to_ref()
        sales_item_line_detail.Qty = qty
        sales_item_line_detail.UnitPrice = unit_price
        today = datetime.now()
        sales_item_line_detail.ServiceDate = today.strftime(
            "%Y-%m-%d"
        )
        line.SalesItemLineDetail = sales_item_line_detail
        line.Amount = qty * unit_price
        sales_receipt.Line = [line]

        return sales_receipt.save(qb=self.qb_client)

    def test_create(self):
        sales_receipt = self.create_sales_receipt(
            qty=1,
            unit_price=100.0
        )
        query_sales_receipt = SalesReceipt.get(sales_receipt.Id, qb=self.qb_client)

        self.assertEqual(query_sales_receipt.TotalAmt, 100.0)
        self.assertEqual(query_sales_receipt.Line[0].Amount, 100.0)
        self.assertEqual(query_sales_receipt.Line[0].SalesItemLineDetail['Qty'], 1)
        self.assertEqual(query_sales_receipt.Line[0].SalesItemLineDetail['UnitPrice'], 100.0)

    def test_void(self):
        sales_receipt = self.create_sales_receipt(
            qty=1,
            unit_price=100.0
        )
        query_sales_receipt = SalesReceipt.get(sales_receipt.Id, qb=self.qb_client)
        self.assertEqual(query_sales_receipt.TotalAmt, 100.0)
        self.assertNotIn('Voided', query_sales_receipt.PrivateNote)
        sales_receipt.void(qb=self.qb_client)
        query_sales_receipt = SalesReceipt.get(sales_receipt.Id, qb=self.qb_client)
        self.assertEqual(query_sales_receipt.TotalAmt, 0.0)
        self.assertIn('Voided', query_sales_receipt.PrivateNote)
