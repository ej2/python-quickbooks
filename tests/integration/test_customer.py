from datetime import datetime
import os
import unittest

from quickbooks.objects.customer import Customer

from quickbooks import QuickBooks


class CustomerTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

        self.title = "Mr"
        self.given_name = "James"
        self.middle_name = "B"
        self.family_name = "King"
        self.suffix = "Jr"
        self.fully_qualified_name = datetime.now().strftime('%d%H%M%S')
        self.company_name = datetime.now().strftime('%d%H%M%S')
        self.display_name = datetime.now().strftime('%d%H%M%S')

    def test_create(self):
        customer = Customer()
        customer.Title = self.title
        customer.GivenName = self.given_name
        customer.MiddleName = self.middle_name
        customer.FamilyName = self.family_name
        customer.Suffix = self.suffix
        customer.FullyQualifiedName = self.fully_qualified_name
        customer.CompanyName = self.company_name
        customer.DisplayName = self.display_name
        customer.save(qb=self.qb_client)

        self.Id = customer.Id

        query_customer = Customer.get(customer.Id, qb=self.qb_client)

        self.assertEquals(customer.Id, query_customer.Id)
        self.assertEqual(query_customer.Title, self.title)
        self.assertEqual(query_customer.GivenName, self.given_name)
        self.assertEqual(query_customer.MiddleName, self.middle_name)
        self.assertEqual(query_customer.FamilyName, self.family_name)
        self.assertEqual(query_customer.Suffix, self.suffix)
        self.assertEqual(query_customer.FullyQualifiedName, self.fully_qualified_name)
        self.assertEqual(query_customer.CompanyName, self.company_name)
        self.assertEqual(query_customer.DisplayName, self.display_name)

    def test_update(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        unique_name = datetime.now().strftime('%d%H%M%S')

        customer.GivenName = unique_name
        customer.save(qb=self.qb_client)

        query_account = Customer.get(customer.Id, qb=self.qb_client)

        self.assertEqual(query_account.GivenName, unique_name)
