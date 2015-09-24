import unittest
from mock import patch
from quickbooks import batch, client
from quickbooks.objects.customer import Customer
from quickbooks.exceptions import QuickbooksException


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.qb = client.QuickBooks(
            sandbox=False,
            consumer_key="consumer_key",
            consumer_secret="consumer_secret",
            access_token="access_token",
            access_token_secret="access_token_secret",
            company_id="company_id",
            callback_url="callback_url",
            verbose=True
        )

        self.object1 = Customer()
        self.object2 = Customer()
        self.obj_list = [self.object1, self.object2]

    def test_invalid_operation(self):
        self.assertRaises(QuickbooksException, batch.BatchManager, "invalid")

    @patch('quickbooks.batch.BatchManager.process_batch')
    def test_batch_create(self, process_batch):
        results = batch.batch_create(self.obj_list)
        self.assertTrue(process_batch.called)

    @patch('quickbooks.batch.BatchManager.process_batch')
    def test_batch_update(self, process_batch):
        results = batch.batch_update(self.obj_list)
        self.assertTrue(process_batch.called)

    @patch('quickbooks.batch.BatchManager.process_batch')
    def test_batch_delete(self, process_batch):
        results = batch.batch_delete(self.obj_list)
        self.assertTrue(process_batch.called)

    def test_list_to_batch_request(self):
        batch_mgr = batch.BatchManager("create")

        obj_list = [self.object1, self.object2]
        batch_request = batch_mgr.list_to_batch_request(obj_list)

        self.assertEquals(len(batch_request.BatchItemRequest), 2)

        batch_item = batch_request.BatchItemRequest[0]
        self.assertTrue(batch_item.bId)
        self.assertTrue(len(batch_item.bId) < 50)
        self.assertEquals(batch_item.operation, "create")
        self.assertEquals(batch_item.get_object(), self.object1)

    def test_batch_results_to_list(self):
        batch_mgr = batch.BatchManager("create")
        json_data = {"BatchItemResponse": [{"Customer": {"Id": 164}, "bId": "2"},
                                           {"Fault": {"type": "ValidationFault",
                                                      "Error": [{"Message": "Duplicate Name Exists Error",
                                                                 "code": "6240", "Detail": "detail message",
                                                                 "element": ""}]}, "bId": "1"}],
                     "time": "2015-08-10T11:44:02.957-07:00"}

        batch_request = batch_mgr.list_to_batch_request(self.obj_list)
        batch_request.BatchItemRequest[0].bId = "1"
        batch_request.BatchItemRequest[1].bId = "2"

        results = batch_mgr.batch_results_to_list(json_data, batch_request, self.obj_list)

        self.assertEquals(len(results.faults), 1)
        self.assertEquals(len(results.successes), 1)
