import os
import unittest
from datetime import datetime

from quickbooks.client import QuickBooks
from quickbooks.objects.term import Term


class TermTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

        self.name = "Term {0}".format(datetime.now().strftime('%d%H%M'))

    def test_create(self):
        term = Term()
        term.Name = self.name
        term.DueDays = 10
        term.save(qb=self.qb_client)

        query_term = Term.get(term.Id, qb=self.qb_client)

        self.assertEquals(query_term.Id, term.Id)
        self.assertEquals(query_term.Name, self.name)
        self.assertEquals(query_term.DueDays, 10)

    def test_update(self):
        term = Term.all(max_results=1, qb=self.qb_client)[0]
        term.DueDays = 60
        term.save(qb=self.qb_client)

        query_term = Term.get(term.Id, qb=self.qb_client)

        self.assertEquals(query_term.Id, term.Id)
        self.assertEquals(query_term.DueDays, 60)
