import unittest

from quickbooks.objects.batchrequest import Fault, FaultError, BatchItemResponse, BatchItemRequest


class FaultErrorTests(unittest.TestCase):
    def test_unicode(self):
        fault_error = FaultError()
        fault_error.Message = "test"
        fault_error.code = 100

        self.assertEquals(unicode(fault_error), "test (100)")


class BatchItemResponseTests(unittest.TestCase):
    def test_set_object(self):
        obj = FaultError()
        batch_item = BatchItemResponse()
        batch_item.set_object(obj)

        self.assertEquals(batch_item._original_object, obj)
        self.assertEquals(batch_item.Error, obj)

    def test_get_object(self):
        obj = Fault()
        batch_item = BatchItemResponse()
        batch_item.set_object(obj)

        self.assertEquals(batch_item.get_object(), obj)


class BatchItemRequestTests(unittest.TestCase):
    def test_set_object(self):
        obj = FaultError()
        batch_item = BatchItemRequest()
        batch_item.set_object(obj)

        self.assertEquals(batch_item._original_object, obj)
        self.assertEquals(batch_item.Error, obj)

    def test_get_object(self):
        obj = Fault()
        batch_item = BatchItemRequest()
        batch_item.set_object(obj)

        self.assertEquals(batch_item.get_object(), obj)
