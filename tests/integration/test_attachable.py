import os
import tempfile
from datetime import datetime

from quickbooks.objects.attachable import Attachable
from quickbooks.objects.base import AttachableRef
from quickbooks.objects.vendor import Vendor
from tests.integration.test_base import QuickbooksTestCase


class AttachableTest(QuickbooksTestCase):
    def setUp(self):
        super(AttachableTest, self).setUp()
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
        test_file = tempfile.NamedTemporaryFile(suffix=".txt")

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]

        attachable_ref = AttachableRef()
        attachable_ref.EntityRef = vendor.to_ref()
        attachable.AttachableRef.append(attachable_ref)

        attachable.FileName = os.path.basename(test_file.name)
        attachable._FilePath = test_file.name
        attachable.ContentType = 'text/plain'

        attachable.save(qb=self.qb_client)

        query_attachable = Attachable.get(attachable.Id, qb=self.qb_client)

        self.assertEquals(query_attachable.AttachableRef[0].EntityRef.value, vendor.Id)
