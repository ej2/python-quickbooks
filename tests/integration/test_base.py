import os
from unittest import TestCase

from intuitlib.client import AuthClient
from quickbooks.client import QuickBooks


class QuickbooksTestCase(TestCase):
    def setUp(self):
        super(QuickbooksTestCase, self).setUp()

        self.auth_client = AuthClient(
            client_id=os.environ.get('CLIENT_ID'),
            client_secret=os.environ.get('CLIENT_SECRET'),
            environment='sandbox',
            redirect_uri='http://localhost:8000/callback',
        )

        self.qb_client = QuickBooks(
            auth_client=self.auth_client,
            refresh_token=os.environ.get('REFRESH_TOKEN'),
            company_id=os.environ.get('COMPANY_ID'),
            sandbox=True,
        )
