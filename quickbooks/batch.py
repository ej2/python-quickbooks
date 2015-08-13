import uuid

from client import QuickBooks
from objects.batchrequest import IntuitBatchRequest, BatchItemRequest, BatchOperation, BatchResponse, BatchItemResponse


def batch_create(obj_list):
    return process_batch(obj_list, BatchOperation.CREATE)


def batch_update(obj_list):
    return process_batch(obj_list, BatchOperation.UPDATE)


def batch_delete(obj_list):
    return process_batch(obj_list, BatchOperation.DELETE)


def process_batch(obj_list, operation):
    qb = QuickBooks()

    batch = list_to_batch_request(obj_list, operation)
    json_data = qb.batch_operation(batch.to_json())

    batch_response = batch_results_to_list(json_data, batch, obj_list)

    return batch_response


def list_to_batch_request(obj_list, operation):
    batch = IntuitBatchRequest()

    for obj in obj_list:
        batch_item = BatchItemRequest()
        batch_item.bId = str(uuid.uuid1())
        batch_item.operation = operation
        batch_item.set_object(obj)

        batch.BatchItemRequest.append(batch_item)

    return batch


def batch_results_to_list(json_data, batch, original_list):
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
            response.successes.append(response_item.get_object())

    return response
