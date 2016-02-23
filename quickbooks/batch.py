import uuid

from .client import QuickBooks
from .exceptions import QuickbooksException
from .objects.batchrequest import IntuitBatchRequest, BatchItemRequest, BatchOperation, BatchResponse, BatchItemResponse


class BatchManager(object):
    def __init__(self, operation, max_request_items=30):
        self._max_request_items = max_request_items

        if operation in ["create", "update", "delete"]:
            self._operation = operation
        else:
            raise QuickbooksException("Operation not supported.")

    def save(self, obj_list, qb=None):
        batch_response = BatchResponse()

        while len(obj_list) > 0:
            temp_list = obj_list[:self._max_request_items]
            obj_list = [item for item in obj_list if item not in temp_list]
            result = self.process_batch(temp_list, qb=qb)

            batch_response.batch_responses += result.batch_responses
            batch_response.original_list += result.original_list
            batch_response.successes += result.successes
            batch_response.faults += result.faults

        return batch_response

    def process_batch(self, obj_list, qb=None):
        if not qb:
            qb = QuickBooks()

        batch = self.list_to_batch_request(obj_list)
        json_data = qb.batch_operation(batch.to_json())
        batch_response = self.batch_results_to_list(json_data, batch, obj_list)

        return batch_response

    def list_to_batch_request(self, obj_list):
        batch = IntuitBatchRequest()

        for obj in obj_list:
            batch_item = BatchItemRequest()
            batch_item.bId = str(uuid.uuid4())
            batch_item.operation = self._operation
            batch_item.set_object(obj)

            batch.BatchItemRequest.append(batch_item)

        return batch

    def batch_results_to_list(self, json_data, batch, original_list):
        response = BatchResponse()
        response.original_list = original_list

        for data in json_data['BatchItemResponse']:
            response_item = BatchItemResponse.from_json(data)

            batch_item = [obj for obj in batch.BatchItemRequest if obj.bId == response_item.bId][0]
            response_item.set_object(batch_item.get_object())

            response.batch_responses.append(response_item)

            if response_item.Fault:
                response_item.Fault.original_object = response_item.get_object()
                response.faults.append(response_item.Fault)

            else:
                class_obj = type(response_item.get_object())
                new_object = class_obj.from_json(data[class_obj.qbo_object_name])
                response.successes.append(new_object)

        return response


def batch_create(obj_list, qb=None):
    batch_mgr = BatchManager(BatchOperation.CREATE)
    return batch_mgr.save(obj_list, qb=qb)


def batch_update(obj_list, qb=None):
    batch_mgr = BatchManager(BatchOperation.UPDATE)
    return batch_mgr.save(obj_list, qb=qb)


def batch_delete(obj_list, qb=None):
    batch_mgr = BatchManager(BatchOperation.DELETE)
    return batch_mgr.save(obj_list, qb=qb)