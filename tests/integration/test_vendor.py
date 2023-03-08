from datetime import datetime

from quickbooks.objects.base import Address, PhoneNumber, EmailAddress, WebAddress
from quickbooks.objects.vendor import Vendor
from tests.integration.test_base import QuickbooksTestCase


class VendorTest(QuickbooksTestCase):
    def setUp(self):
        super(VendorTest, self).setUp()

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

        self.assertEqual(query_vendor.Id, vendor.Id)

        self.assertEqual(query_vendor.AcctNum, self.account_number)
        self.assertEqual(query_vendor.Title, 'Ms.')
        self.assertEqual(query_vendor.GivenName, 'First')
        self.assertEqual(query_vendor.FamilyName, 'Last')
        self.assertEqual(query_vendor.Suffix, 'Sr.')
        self.assertEqual(query_vendor.CompanyName, self.name)
        self.assertEqual(query_vendor.DisplayName, self.name)
        self.assertEqual(query_vendor.PrintOnCheckName, self.name)

        self.assertEqual(query_vendor.BillAddr.Line1, "123 Main")
        self.assertEqual(query_vendor.BillAddr.Line2, "Apartment 1")
        self.assertEqual(query_vendor.BillAddr.City, "City")
        self.assertEqual(query_vendor.BillAddr.Country, "U.S.A")
        self.assertEqual(query_vendor.BillAddr.CountrySubDivisionCode, "CA")
        self.assertEqual(query_vendor.BillAddr.PostalCode, "94030")
        self.assertEqual(query_vendor.PrimaryPhone.FreeFormNumber, '555-555-5555')
        self.assertEqual(query_vendor.PrimaryEmailAddr.Address, 'test@email.com')
        self.assertEqual(query_vendor.WebAddr.URI, 'http://testurl.com')

    def update_vendor(self):
        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]

        vendor.GivenName = 'Updated Name'
        vendor.FamilyName = 'Updated Lastname'

        vendor.save(qb=self.qb_client)

        query_vendor = Vendor.get(vendor.Id, qb=self.qb_client)
        self.assertEqual(query_vendor.GivenName, 'Updated Name')
        self.assertEqual(query_vendor.FamilyName, 'Updated Lastname')
