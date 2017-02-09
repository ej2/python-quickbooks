from datetime import datetime
from .client import QuickBooks

class CDCManager(object):
	pass



def change_data_capture(qbo_class_list, timestamp, qb=None):

	if qb is None:
		qb = QuickBooks()

	entity_list_string = ','.join([x.qbo_object_name for x in qbo_class_list])
	print(entity_list_string)

	if isinstance(datetime, datetime):
		timestamp_string = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
	else:
		timestamp_string = timestamp

	raw = qb.change_data_capture(entity_list_string, timestamp_string)
