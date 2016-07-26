import os
import unittest
from datetime import datetime

from quickbooks.objects.detailline import DetailLine, SalesItemLineDetail, DiscountLineDetail, SalesItemLine

from quickbooks.objects.tax import TxnTaxDetail

from quickbooks.objects.customer import Customer

from quickbooks.objects.base import Address, EmailAddress, CustomerMemo, Ref

from quickbooks.objects.estimate import Estimate

from quickbooks import QuickBooks


class BillTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )
        self.customer = Customer.all(max_results=1, qb=self.qb_client)[0]

    def test_create(self):
        estimate = Estimate()
        estimate.TotalAmt = 31.5
        estimate.ApplyTaxAfterDiscount = False
        estimate.PrintStatus = "NeedToPrint"
        estimate.EmailStatus = "NotSet"

        estimate.BillAddr = Address()
        # estimate.BillAddr.Id = "1" + datetime.now().strftime('%d%H%M')
        estimate.BillAddr.Line1 = "65 Ocean Dr."
        estimate.BillAddr.City = "Half Moon Bay"
        estimate.BillAddr.CountrySubDivisionCode = "CA"
        estimate.BillAddr.PostalCode = "94213"
        estimate.BillAddr.Lat = "37.4300318"
        estimate.BillAddr.Long = "-122.4336537"

        estimate.ShipAddr = Address()
        estimate.ShipAddr.Id = "2" + datetime.now().strftime('%d%H%M')
        estimate.ShipAddr.Line1 = "65 Ocean Dr."
        estimate.ShipAddr.City = "Half Moon Bay"
        estimate.ShipAddr.CountrySubDivisionCode = "CA"
        estimate.ShipAddr.PostalCode = "94213"
        estimate.ShipAddr.Lat = "37.4300318"
        estimate.ShipAddr.Long = "-122.4336537"

        estimate.BillEmail = EmailAddress()
        estimate.BillEmail.Address = "Cool_Cars@intuit.com"

        estimate.CustomerMemo = CustomerMemo()
        estimate.CustomerMemo.value = "Thank you for your business and have a great day!"

        estimate.CustomerRef = Ref()
        estimate.CustomerRef.value = self.customer.Id
        estimate.CustomerRef.name = self.customer.DisplayName

        estimate.TxnTaxDetail = TxnTaxDetail()
        estimate.TxnTaxDetail.TotalTax = 0

        line = SalesItemLine()
        line.LineNum = 1
        line.Description = "Pest Control Services"
        line.Amount = 35.0

        line.SalesItemLineDetail = SalesItemLineDetail()
        line.SalesItemLineDetail.UnitPrice = 35
        line.SalesItemLineDetail.Qty = 1

        item_ref = Ref()
        item_ref.value = "10"
        item_ref.name = "Pest Control"
        line.SalesItemLineDetail.ItemRef = item_ref

        tax_code_ref = Ref()
        tax_code_ref.value = "NON"
        line.SalesItemLineDetail.TaxCodeRef = tax_code_ref

        estimate.Line.append(line)

        line2 = DetailLine()
        line2.Amount = 3.5

        discount_line_detail = DiscountLineDetail()
        discount_line_detail.PercentBased = True
        discount_line_detail.DiscountPercent = 10

        discount_account_ref = Ref()
        discount_account_ref.value = "86"
        discount_account_ref.name = "Discounts given"
        discount_line_detail.DiscountAccountRef = discount_account_ref

        line2.DetailType = "DiscountLineDetail"
        line2.DiscountLineDetail = discount_line_detail
        estimate.Line.append(line2)

        estimate.save(qb=self.qb_client)

        query_estimate = Estimate.get(estimate.Id, qb=self.qb_client)

        self.assertEqual(query_estimate.Id, estimate.Id)
        self.assertEqual(query_estimate.TotalAmt, estimate.TotalAmt)
        self.assertEqual(query_estimate.ApplyTaxAfterDiscount, estimate.ApplyTaxAfterDiscount)
        self.assertEqual(query_estimate.PrintStatus, estimate.PrintStatus)
        self.assertEqual(query_estimate.EmailStatus, estimate.EmailStatus)
        # self.assertEqual(query_estimate.BillAddr.Id, estimate.BillAddr.Id)
        self.assertEqual(query_estimate.BillAddr.Line1, estimate.BillAddr.Line1)
        self.assertEqual(query_estimate.BillAddr.City, estimate.BillAddr.City)
        self.assertEqual(query_estimate.BillAddr.CountrySubDivisionCode, estimate.BillAddr.CountrySubDivisionCode)
        self.assertEqual(query_estimate.BillAddr.PostalCode, estimate.BillAddr.PostalCode)
        # self.assertEqual(query_estimate.BillAddr.Lat, estimate.BillAddr.Lat)
        # self.assertEqual(query_estimate.BillAddr.Long, estimate.BillAddr.Long)
        # self.assertEqual(query_estimate.ShipAddr.Id, estimate.ShipAddr.Id)
        self.assertEqual(query_estimate.ShipAddr.Line1, estimate.ShipAddr.Line1)
        self.assertEqual(query_estimate.ShipAddr.City, estimate.ShipAddr.City)
        self.assertEqual(query_estimate.ShipAddr.CountrySubDivisionCode, estimate.ShipAddr.CountrySubDivisionCode)
        self.assertEqual(query_estimate.ShipAddr.PostalCode, estimate.ShipAddr.PostalCode)
        # self.assertEqual(query_estimate.ShipAddr.Lat, estimate.ShipAddr.Lat)
        # self.assertEqual(query_estimate.ShipAddr.Long, estimate.ShipAddr.Long)
        self.assertEqual(query_estimate.BillEmail.Address, estimate.BillEmail.Address)
        self.assertEqual(query_estimate.CustomerMemo.value, estimate.CustomerMemo.value)
        self.assertEqual(query_estimate.CustomerRef.value, estimate.CustomerRef.value)
        self.assertEqual(query_estimate.CustomerRef.name, estimate.CustomerRef.name)
        self.assertEqual(query_estimate.TxnTaxDetail.TotalTax, estimate.TxnTaxDetail.TotalTax)
        self.assertEqual(query_estimate.Line[0].LineNum, estimate.Line[0].LineNum)
        self.assertEqual(query_estimate.Line[0].Description, estimate.Line[0].Description)
        self.assertEqual(query_estimate.Line[0].Amount, estimate.Line[0].Amount)
        # self.assertEqual(query_estimate.Line[0].SalesItemLineDetail.UnitPrice,
        #                  estimate.Line[0].SalesItemLineDetail.UnitPrice)
        # self.assertEqual(query_estimate.Line[0].SalesItemLineDetail.Qty, estimate.Line[0].SalesItemLineDetail.Qty)
