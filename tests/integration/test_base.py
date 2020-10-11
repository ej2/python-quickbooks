import os
from unittest import TestCase

from intuitlib.client import AuthClient
from quickbooks.client import QuickBooks, Environments


class QuickbooksTestCase(TestCase):
    def setUp(self):
        super(QuickbooksTestCase, self).setUp()

        self.auth_client = AuthClient(
            client_id=os.environ.get('CLIENT_ID'),
            client_secret=os.environ.get('CLIENT_SECRET'),
            environment=Environments.SANDBOX,
            redirect_uri='http://localhost:8000/callback',
        )

        self.qb_client = QuickBooks(
            minorversion=54,
            auth_client=self.auth_client,
            refresh_token=os.environ.get('REFRESH_TOKEN'),
            company_id=os.environ.get('COMPANY_ID'),
        )

        self.qb_client.sandbox = True


class QuickbooksUnitTestCase(TestCase):
    def setUp(self):
        super(QuickbooksUnitTestCase, self).setUp()

        self.auth_client = AuthClient(
            client_id='CLIENTID',
            client_secret='CLIENT_SECRET',
            environment=Environments.SANDBOX,
            redirect_uri='http://localhost:8000/callback',
        )

        self.qb_client = QuickBooks(
            #auth_client=self.auth_client,
            refresh_token='REFRESH_TOKEN',
            company_id='COMPANY_ID',
        )

        self.qb_client.sandbox = True
