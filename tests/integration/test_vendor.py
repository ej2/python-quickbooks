import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.base import Address, PhoneNumber, EmailAddress, WebAddress
from quickbooks.objects.vendor import Vendor


class VendorTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
        )

        self.qb_client = QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id=os.environ.get('COMPANY_ID')
        )

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Vendor {0}".format(self.account_number)

    def test_create(self):
        vendor = Vendor()

        vendor.TaxIdentifier = '99-9999999'
        vendor.AcctNum = self.account_number
        vendor.Title = 'Ms.'
        vendor.GivenName = 'First'
        vendor.FamilyName = 'Last'
        vendor.Suffix = 'Sr.'
        vendor.CompanyName = self.name
        vendor.DisplayName = self.name
        vendor.PrintOnCheckName = self.name

        vendor.BillAddr = Address()
        vendor.BillAddr.Line1 = "123 Main"
        vendor.BillAddr.Line2 = "Apartment 1"
        vendor.BillAddr.City = "City"
        vendor.BillAddr.Country = "U.S.A"
        vendor.BillAddr.CountrySubDivisionCode = "CA"
        vendor.BillAddr.PostalCode = "94030"

        vendor.PrimaryPhone = PhoneNumber()
        vendor.PrimaryPhone.FreeFormNumber = '555-555-5555'

        vendor.PrimaryEmailAddr = EmailAddress()
        vendor.PrimaryEmailAddr.Address = 'test@email.com'

        vendor.WebAddr = WebAddress()
        vendor.WebAddr.URI = 'http://testurl.com'

        vendor.save(qb=self.qb_client)

        query_vendor = Vendor.get(vendor.Id, qb=self.qb_client)

        self.assertEquals(query_vendor.Id, vendor.Id)

        self.assertEquals(query_vendor.AcctNum, self.account_number)
        self.assertEquals(query_vendor.Title, 'Ms.')
        self.assertEquals(query_vendor.GivenName, 'First')
        self.assertEquals(query_vendor.FamilyName, 'Last')
        self.assertEquals(query_vendor.Suffix, 'Sr.')
        self.assertEquals(query_vendor.CompanyName, self.name)
        self.assertEquals(query_vendor.DisplayName, self.name)
        self.assertEquals(query_vendor.PrintOnCheckName, self.name)

        self.assertEquals(query_vendor.BillAddr.Line1, "123 Main")
        self.assertEquals(query_vendor.BillAddr.Line2, "Apartment 1")
        self.assertEquals(query_vendor.BillAddr.City, "City")
        self.assertEquals(query_vendor.BillAddr.Country, "U.S.A")
        self.assertEquals(query_vendor.BillAddr.CountrySubDivisionCode, "CA")
        self.assertEquals(query_vendor.BillAddr.PostalCode, "94030")
        self.assertEquals(query_vendor.PrimaryPhone.FreeFormNumber, '555-555-5555')
        self.assertEquals(query_vendor.PrimaryEmailAddr.Address, 'test@email.com')
        self.assertEquals(query_vendor.WebAddr.URI, 'http://testurl.com')

    def update_vendor(self):
        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]

        vendor.GivenName = 'Updated Name'
        vendor.FamilyName = 'Updated Lastname'

        vendor.save(qb=self.qb_client)

        query_vendor = Vendor.get(vendor.Id, qb=self.qb_client)
        self.assertEquals(query_vendor.GivenName, 'Updated Name')
        self.assertEquals(query_vendor.FamilyName, 'Updated Lastname')
