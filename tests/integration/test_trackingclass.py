from datetime import datetime

from quickbooks.objects.trackingclass import Class
from tests.integration.test_base import QuickbooksTestCase


class ClassTest(QuickbooksTestCase):
    def setUp(self):
        super(ClassTest, self).setUp()

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
