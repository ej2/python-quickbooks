from quickbooks.objects.account import Account
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import ItemBasedExpenseLine, ItemBasedExpenseLineDetail
from quickbooks.objects.item import Item
from quickbooks.objects.purchase import Purchase
from quickbooks.objects.taxcode import TaxCode
from tests.integration.test_base import QuickbooksTestCase


class PurchaseOrderTest(QuickbooksTestCase):
    def test_create(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        taxcode = TaxCode.all(max_results=1, qb=self.qb_client)[0]
        item = Item.filter(Type='Inventory', max_results=1, qb=self.qb_client)[0]

        credit_account = Account()
        credit_account.FullyQualifiedName = 'Visa'
        credit_account.Id = "42"

        purchase = Purchase()
        purchase.DocNumber = "Doc123"
        purchase.PaymentType = "CreditCard"
        purchase.AccountRef = credit_account.to_ref()
        purchase.TotalAmt = 100

        detail_line = ItemBasedExpenseLine()
        detail_line.Amount = 100
        detail_line.ItemBasedExpenseLineDetail = ItemBasedExpenseLineDetail()
        detail_line.ItemBasedExpenseLineDetail.BillableStatus = "NotBillable"
        detail_line.ItemBasedExpenseLineDetail.UnitPrice = 100
        detail_line.ItemBasedExpenseLineDetail.Qty = 1
        detail_line.ItemBasedExpenseLineDetail.CustomerRef = customer.to_ref()
        detail_line.ItemBasedExpenseLineDetail.TaxCodeRef = taxcode.to_ref()
        detail_line.ItemBasedExpenseLineDetail.ItemRef = item.to_ref()

        purchase.Line.append(detail_line)

        print(purchase.to_json())
        purchase.save(qb=self.qb_client, params={'include': 'allowduplicatedocnum'})

        query_purchase = Purchase.get(purchase.Id, qb=self.qb_client)

        self.assertEqual(query_purchase.AccountRef.value, credit_account.Id)
        self.assertEqual(query_purchase.DocNumber, "Doc123")
        self.assertEqual(query_purchase.TotalAmt, 100)

        query_detail_line = query_purchase.Line[0]

        self.assertEqual(query_detail_line.Amount, 100)
        self.assertEqual(query_detail_line.ItemBasedExpenseLineDetail.UnitPrice, 100)
        self.assertEqual(query_detail_line.ItemBasedExpenseLineDetail.Qty, 1)
        self.assertEqual(query_detail_line.ItemBasedExpenseLineDetail.CustomerRef.value, customer.Id)
        self.assertEqual(query_detail_line.ItemBasedExpenseLineDetail.TaxCodeRef.value, taxcode.Name)
        self.assertEqual(query_detail_line.ItemBasedExpenseLineDetail.ItemRef.value, item.Id)


