from datetime import datetime

from quickbooks.objects.term import Term
from tests.integration.test_base import QuickbooksTestCase


class TermTest(QuickbooksTestCase):
    def setUp(self):
        super(TermTest, self).setUp()

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
