import os
import unittest
from datetime import datetime

from quickbooks.client import QuickBooks
from quickbooks.objects.attachable import Attachable
from quickbooks.objects.base import Ref, AttachableRef
from quickbooks.objects.vendor import Vendor


class AttachableTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

        self.time = datetime.now()

    def test_create_note(self):
        attachable = Attachable()

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]

        attachable_ref = AttachableRef()
        attachable_ref.EntityRef = vendor.to_ref()
        attachable.AttachableRef.append(attachable_ref)

        attachable.Note = "Test note added on {}".format(self.time.strftime("%Y-%m-%d %H:%M:%S"))

        attachable.save(qb=self.qb_client)
        query_attachable = Attachable.get(attachable.Id, qb=self.qb_client)

        self.assertEquals(query_attachable.AttachableRef[0].EntityRef.value, vendor.Id)
        self.assertEquals(query_attachable.Note, "Test note added on {}".format(self.time.strftime("%Y-%m-%d %H:%M:%S")))

    def test_update_note(self):
        attachable = Attachable.all(max_results=1, qb=self.qb_client)[0]

        attachable.Note = "Note updated on {}".format(self.time.strftime("%Y-%m-%d %H:%M:%S"))
        attachable.save(qb=self.qb_client)

        query_attachable = Attachable.get(attachable.Id, qb=self.qb_client)
        self.assertEquals(query_attachable.Note, "Note updated on {}".format(self.time.strftime("%Y-%m-%d %H:%M:%S")))

    def test_create_file(self):
        attachable = Attachable()

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]

        attachable_ref = AttachableRef()
        attachable_ref.EntityRef = vendor.to_ref()
        attachable.AttachableRef.append(attachable_ref)

        attachable.FileName = 'TestFileName'
        attachable._FilePath = __file__
        attachable.ContentType = 'application/txt'

        attachable.save(qb=self.qb_client)
        query_attachable = Attachable.get(attachable.Id, qb=self.qb_client)

        self.assertEquals(query_attachable.AttachableRef[0].EntityRef.value, vendor.Id)
