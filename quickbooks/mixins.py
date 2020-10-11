from future.moves.urllib.parse import quote

try: import simplejson as json
except ImportError: import json

import six
from .utils import build_where_clause, build_choose_clause
from .client import QuickBooks
from .exceptions import QuickbooksException


class ToJsonMixin(object):
    def to_json(self):
        return json.dumps(self, default=self.json_filter(), sort_keys=True, indent=4)

    def json_filter(self):
        """
        filter out properties that have names starting with _
        or properties that have a value of None
        """
        return lambda obj: dict((k, v) for k, v in obj.__dict__.items()
                                if not k.startswith('_') and getattr(obj, k) is not None)


class FromJsonMixin(object):
    class_dict = {}
    list_dict = {}

    @classmethod
    def from_json(cls, json_data):
        obj = cls()
        for key in json_data:
            if key in obj.class_dict:
                sub_obj = obj.class_dict[key]()
                sub_obj = sub_obj.from_json(json_data[key])
                setattr(obj, key, sub_obj)

            elif key in obj.list_dict:
                sub_list = []

                for data in json_data[key]:

                    if 'DetailType' in data and data['DetailType'] in obj.detail_dict:
                        sub_obj = obj.detail_dict[data['DetailType']]()
                    else:
                        sub_obj = obj.list_dict[key]()

                    sub_obj = sub_obj.from_json(data)
                    sub_list.append(sub_obj)

                setattr(obj, key, sub_list)
            else:
                setattr(obj, key, json_data[key])

        return obj


# Based on http://stackoverflow.com/a/1118038
def to_dict(obj, classkey=None):
    """
    Recursively converts Python object into a dictionary
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_dict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        if six.PY2:
            data = dict([(key, to_dict(value, classkey))
                        for key, value in obj.__dict__.iteritems()
                        if not callable(value) and not key.startswith('_')])
        else:
            data = dict([(key, to_dict(value, classkey))
                        for key, value in obj.__dict__.items()
                        if not callable(value) and not key.startswith('_')])

        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


class ToDictMixin(object):
    def to_dict(self):
        return to_dict(self)


class ReadMixin(object):
    qbo_object_name = ""
    qbo_json_object_name = ""

    @classmethod
    def get(cls, id, qb=None):
        if not qb:
            qb = QuickBooks()

        json_data = qb.get_single_object(cls.qbo_object_name, pk=id)

        if cls.qbo_json_object_name != '':
            return cls.from_json(json_data[cls.qbo_json_object_name])
        else:
            return cls.from_json(json_data[cls.qbo_object_name])


class SendMixin(object):
    def send(self, qb=None, send_to=None):
        if not qb:
            qb = QuickBooks()

        end_point = "{0}/{1}/send".format(self.qbo_object_name.lower(), self.Id)

        if send_to:
            send_to = quote(send_to, safe='')
            end_point = "{0}?sendTo={1}".format(end_point, send_to)

        results = qb.misc_operation(end_point, None, 'application/octet-stream')

        return results


class VoidMixin(object):
    def void(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if not self.Id:
            raise QuickbooksException('Cannot void unsaved object')

        data = {
            'Id': self.Id,
            'SyncToken': self.SyncToken,
        }

        endpoint = self.qbo_object_name.lower()
        url = "{0}/company/{1}/{2}".format(qb.api_url, qb.company_id, endpoint)
        results = qb.post(url, json.dumps(data), params={'operation': 'void'})

        return results


class UpdateMixin(object):
    qbo_object_name = ""
    qbo_json_object_name = ""

    def save(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if self.Id and int(self.Id) > 0:
            json_data = qb.update_object(self.qbo_object_name, self.to_json())
        else:
            json_data = qb.create_object(self.qbo_object_name, self.to_json())

        if self.qbo_json_object_name != '':
            obj = type(self).from_json(json_data[self.qbo_json_object_name])
        else:
            obj = type(self).from_json(json_data[self.qbo_object_name])

        self.Id = obj.Id
        return obj


class DeleteMixin(object):
    qbo_object_name = ""

    def delete(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if not self.Id:
            raise QuickbooksException('Cannot delete unsaved object')

        data = {
            'Id': self.Id,
            'SyncToken': self.SyncToken,
        }
        return qb.delete_object(self.qbo_object_name, json.dumps(data))


class ListMixin(object):
    qbo_object_name = ""
    qbo_json_object_name = ""

    @classmethod
    def all(cls, order_by="", start_position="", max_results=100, qb=None):
        """
        :param start_position:
        :param max_results: The max number of entities that can be returned in a response is 1000.
        :param qb:
        :return: Returns list
        """
        return cls.where("", order_by=order_by, start_position=start_position,
                         max_results=max_results, qb=qb)

    @classmethod
    def filter(cls, order_by="", start_position="", max_results="", qb=None, **kwargs):
        """
        :param order_by:
        :param start_position:
        :param max_results:
        :param qb:
        :param kwargs: field names and values to filter the query
        :return: Filtered list
        """
        return cls.where(build_where_clause(**kwargs),
                         start_position=start_position, max_results=max_results, order_by=order_by,
                         qb=qb)

    @classmethod
    def choose(cls, choices, field="Id", qb=None):
        """
        :param choices:
        :param field:
        :param qb:
        :return: Filtered list
        """
        return cls.where(build_choose_clause(choices, field), qb=qb)

    @classmethod
    def where(cls, where_clause="", order_by="", start_position="", max_results="", qb=None):
        """
        :param where_clause: QBO SQL where clause (DO NOT include 'WHERE')
        :param order_by:
        :param start_position:
        :param max_results:
        :param qb:
        :return: Returns list filtered by input where_clause
        """
        if where_clause:
            where_clause = "WHERE " + where_clause

        if order_by:
            order_by = " ORDERBY " + order_by

        if start_position != "":
            start_position = " STARTPOSITION " + str(start_position)

        if max_results:
            max_results = " MAXRESULTS " + str(max_results)

        select = "SELECT * FROM {0} {1}{2}{3}{4}".format(
            cls.qbo_object_name, where_clause, order_by, start_position, max_results)

        return cls.query(select, qb=qb)

    @classmethod
    def query(cls, select, qb=None):
        """
        :param select: QBO SQL query select statement
        :param qb:
        :return: Returns list
        """
        if not qb:
            qb = QuickBooks()

        json_data = qb.query(select)

        obj_list = []

        if cls.qbo_json_object_name != '':
            object_name = cls.qbo_json_object_name
        else:
            object_name = cls.qbo_object_name

        if object_name in json_data["QueryResponse"]:
            for item_json in json_data["QueryResponse"][object_name]:
                obj_list.append(cls.from_json(item_json))

        return obj_list

    @classmethod
    def count(cls, where_clause="", qb=None):
        """
        :param where_clause: QBO SQL where clause (DO NOT include 'WHERE')
        :param qb:
        :return: Returns database record count
        """
        if not qb:
            qb = QuickBooks()

        if where_clause:
            where_clause = "WHERE " + where_clause

        select = "SELECT COUNT(*) FROM {0} {1}".format(
            cls.qbo_object_name, where_clause)

        json_data = qb.query(select)

        if "totalCount" in json_data["QueryResponse"]:
            return json_data["QueryResponse"]["totalCount"]
        else:
            return None


class QuickbooksPdfDownloadable(object):
    qbo_object_name = ""

    def download_pdf(self, qb=None):
        if self.Id and int(self.Id) > 0 and qb is not None:
            return qb.download_pdf(self.qbo_object_name, self.Id)
        else:
            raise QuickbooksException(
                "Cannot download {0} when no Id is assigned or if no quickbooks client is passed in".format(
                    self.qbo_object_name))


class ObjectListMixin(object):
    qbo_object_name = ""
    _object_list = []

    def __iter__(self):
        return self._object_list.__iter__()

    def __len__(self):
        return self._object_list.__len__()

    def __contains__(self, item):
        return self._object_list.__contains__(item)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self._object_list.__getitem__(key)

    def __setitem__(self, key, value):
        self._object_list.__setitem__(key, value)

    def __delitem__(self, key):
        self._object_list.__delitem__(key)

    def __reversed__(self):
        return self._object_list.__reversed__()

    def append(self, value):
        self._object_list.append(value)

    def pop(self, *args, **kwargs):
        return self._object_list.pop(*args, **kwargs)
