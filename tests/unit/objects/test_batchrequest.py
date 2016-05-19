import unittest

from quickbooks.objects.batchrequest import Fault, FaultError, BatchItemResponse, BatchItemRequest


class FaultTests(unittest.TestCase):
    def test__repr__(self):
        fault = Fault()
        fault.type = "test"
        fault.original_object = 100
        fault.Error.append("error")

        self.assertEquals(str(fault.__repr__()), "1 Errors")


class FaultErrorTests(unittest.TestCase):
    def test_unicode(self):
        fault_error = FaultError()
        fault_error.Message = "test"
        fault_error.code = 100
        fault_error.Detail = "detail"

        self.assertEquals(str(fault_error), "Code: 100 Message: test Detail: detail")

    def test__repr__(self):
        fault_error = FaultError()
        fault_error.Message = "test"
        fault_error.code = 100
        fault_error.Detail = "detail"

        self.assertEquals(fault_error.__repr__(), "Code: 100 Message: test Detail: detail")


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
