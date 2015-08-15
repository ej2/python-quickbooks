import unittest
from mock import patch
from quickbooks import batch, client
from quickbooks.objects.customer import Customer

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

    @patch('quickbooks.batch.process_batch')
    def test_batch_create(self, process_batch):
        results = batch.batch_create(self.obj_list)
        self.assertTrue(process_batch.called)

    @patch('quickbooks.batch.process_batch')
    def test_batch_update(self, process_batch):
        results = batch.batch_update(self.obj_list)
        self.assertTrue(process_batch.called)

    @patch('quickbooks.batch.process_batch')
    def test_batch_delete(self, process_batch):
        results = batch.batch_delete(self.obj_list)
        self.assertTrue(process_batch.called)

    def test_process_batch(self):
        pass

    def test_list_to_batch_request(self):
        obj_list = [self.object1, self.object2]
        batch_request = batch.list_to_batch_request(obj_list, "create")

        self.assertEquals(len(batch_request.BatchItemRequest), 2)

        batch_item = batch_request.BatchItemRequest[0]
        self.assertTrue(batch_item.bId)
        self.assertEquals(batch_item.operation, "create")
        self.assertEquals(batch_item.get_object(), self.object1)

    # def test_batch_results_to_list(self):
    #     json_data = '{ "BatchItemResponse": [ {"Customer":{"Id": 164}, "bId":"2"}, ' \
    #                 '{"Fault": {"type": "ValidationFault","Error": [{"Message": "Duplicate Name Exists Error",' \
    #                 '"code": "6240","Detail": "detail message", "element": ""}]},"bId": "1" } ],' \
    #                 '"time": "2015-08-10T11:44:02.957-07:00"}'
    #
    #     batch_request = batch.list_to_batch_request(self.obj_list, "create")
    #     results = batch.batch_results_to_list(json_data, batch_request, self.obj_list)
    #
    #     self.assertEquals(len(results.faults), 1)
    #     self.assertEquals(len(results.successes), 1)