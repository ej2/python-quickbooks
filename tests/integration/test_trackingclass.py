import os
import unittest
from datetime import datetime

from quickbooks.auth import Oauth1SessionManager
from quickbooks.client import QuickBooks
from quickbooks.objects.trackingclass import Class


class ClassTest(unittest.TestCase):
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

        self.name = "Test Class {0}".format(datetime.now().strftime('%d%H%M'))

    def test_create(self):
        tracking_class = Class()
        tracking_class.Name = self.name
        tracking_class.save(qb=self.qb_client)

        query_tracking_class = Class.get(tracking_class.Id, qb=self.qb_client)

        self.assertEquals(query_tracking_class.Id, tracking_class.Id)
        self.assertEquals(query_tracking_class.Name, self.name)

    def test_update(self):
        updated_name = "Updated {}".format(self.name)

        tracking_class = Class.all(max_results=1, qb=self.qb_client)[0]
        tracking_class.Name = updated_name
        tracking_class.save(qb=self.qb_client)

        query_tracking_class = Class.get(tracking_class.Id, qb=self.qb_client)

        self.assertEquals(query_tracking_class.Id, tracking_class.Id)
        self.assertEquals(query_tracking_class.Name, updated_name)
