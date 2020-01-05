from datetime import datetime
from .client import QuickBooks
from .objects.changedatacapture import QueryResponse, CDCResponse
from .helpers import qb_datetime_format


def change_data_capture(qbo_class_list, timestamp, qb=None):
    if qb is None:
        qb = QuickBooks()

    cdc_class_dict = dict((cls.qbo_object_name, cls) for cls in qbo_class_list)

    cdc_class_names = list(cdc_class_dict.keys())
    entity_list_string = ','.join(cdc_class_names)

    if isinstance(timestamp, datetime):
        timestamp_string = qb_datetime_format(timestamp)
    else:
        timestamp_string = timestamp

    resp = qb.change_data_capture(entity_list_string, timestamp_string)

    cdc_response_dict = resp.pop('CDCResponse')
    cdc_response = CDCResponse.from_json(resp)

    query_response_list = cdc_response_dict[0]['QueryResponse']
    for query_response_dict in query_response_list:
        qb_object_names = [x for x in query_response_dict if x in cdc_class_names]

        if len(qb_object_names) == 1:
            qb_object_name = qb_object_names[0]
            qb_object_list = query_response_dict.pop(qb_object_name)
            qb_object_cls = cdc_class_dict[qb_object_name]

            query_response = QueryResponse.from_json(query_response_dict)
            query_response._object_list = [qb_object_cls.from_json(obj) for obj in qb_object_list]

            setattr(cdc_response, qb_object_name, query_response)

    return cdc_response
