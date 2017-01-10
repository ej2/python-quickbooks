import os
import unittest

from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import ItemBasedExpenseLine, ItemBasedExpenseLineDetail
from quickbooks.objects.item import Item
from quickbooks.objects.purchaseorder import PurchaseOrder
from quickbooks.objects.taxcode import TaxCode
from quickbooks.objects.vendor import Vendor


class PurchaseOrderTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

    def test_create(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        taxcode = TaxCode.all(max_results=1, qb=self.qb_client)[0]
        item = Item.filter(Type='Inventory', max_results=1, qb=self.qb_client)[0]
        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        account = Account.all(max_results=1, qb=self.qb_client)[0]

        purchaseorder = PurchaseOrder()

        detail_line = ItemBasedExpenseLine()
        detail_line.Amount = 100
        detail_line.ItemBasedExpenseLineDetail = ItemBasedExpenseLineDetail()
        detail_line.ItemBasedExpenseLineDetail.BillableStatus = "NotBillable"
        detail_line.ItemBasedExpenseLineDetail.UnitPrice = 100
        detail_line.ItemBasedExpenseLineDetail.Qty = 1
        detail_line.ItemBasedExpenseLineDetail.CustomerRef = customer.to_ref()
        detail_line.ItemBasedExpenseLineDetail.TaxCodeRef = taxcode.to_ref()
        detail_line.ItemBasedExpenseLineDetail.ItemRef = item.to_ref()

        purchaseorder.Line.append(detail_line)
        purchaseorder.VendorRef = vendor.to_ref()
        purchaseorder.APAccountRef = account.to_ref()
        purchaseorder.TotalAmt = 100

        print purchaseorder.to_json()
        purchaseorder.save(qb=self.qb_client)

        query_purchaseorder = PurchaseOrder.get(purchaseorder.Id, qb=self.qb_client)

        self.assertEquals(query_purchaseorder.VendorRef.value, vendor.Id)
        self.assertEquals(query_purchaseorder.APAccountRef.value, account.Id)
        self.assertEquals(query_purchaseorder.TotalAmt, 100)

        query_detail_line = query_purchaseorder.Line[0]

        self.assertEquals(query_detail_line.Amount, 100)
        self.assertEquals(query_detail_line.ItemBasedExpenseLineDetail.UnitPrice, 100)
        self.assertEquals(query_detail_line.ItemBasedExpenseLineDetail.Qty, 1)
        self.assertEquals(query_detail_line.ItemBasedExpenseLineDetail.CustomerRef.value, customer.Id)
        self.assertEquals(query_detail_line.ItemBasedExpenseLineDetail.TaxCodeRef.value, taxcode.Name)
        self.assertEquals(query_detail_line.ItemBasedExpenseLineDetail.ItemRef.value, item.Id)


