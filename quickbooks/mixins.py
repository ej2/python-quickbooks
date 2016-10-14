import simplejson as json
from .utils import build_where_clause, build_choose_clause
from .client import QuickBooks
from .exceptions import QuickbooksException


class ToJsonMixin(object):
    def to_json(self):
        return json.dumps(self, default=self.json_filter(), sort_keys=True, indent=4)

    def json_filter(self):
        """
        filter out properties that have names starting with _ or properties that have a value of None
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


class ReadMixin(object):
    qbo_object_name = ""

    @classmethod
    def get(cls, id, qb=None):
        if not qb:
            qb = QuickBooks()

        json_data = qb.get_single_object(cls.qbo_object_name, pk=id)
        return cls.from_json(json_data[cls.qbo_object_name])


class UpdateMixin(object):
    qbo_object_name = ""

    def save(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if self.Id and int(self.Id) > 0:
            json_data = qb.update_object(self.qbo_object_name, self.to_json())
        else:
            json_data = qb.create_object(self.qbo_object_name, self.to_json())

        obj = type(self).from_json(json_data[self.qbo_object_name])
        self.Id = obj.Id

        return obj


class ListMixin(object):
    qbo_object_name = ""

    @classmethod
    def all(cls, start_position="", max_results=100, qb=None):
        """
        :param max_results: The maximum number of entities that can be returned in a response is 1000.
        :return: Returns list
        """
        return cls.where("", start_position=start_position, max_results=max_results, qb=qb)

    @classmethod
    def filter(cls, start_position="", max_results="", qb=None, **kwargs):
        """
        :param kwargs: field names and values to filter the query
        :return: Filtered list
        """
        return cls.where(build_where_clause(**kwargs), start_position=start_position, max_results=max_results, qb=qb)

    @classmethod
    def choose(cls, choices, field="Id", qb=None):
        """
        :param kwargs: field names and values to filter the query
        :return: Filtered list
        """
        return cls.where(build_choose_clause(choices, field), qb=qb)

    @classmethod
    def where(cls, where_clause="", start_position="", max_results="", qb=None):
        """
        :param where_clause: QBO SQL where clause (DO NOT include 'WHERE')
        :return: Returns list filtered by input where_clause
        """
        if where_clause:
            where_clause = "WHERE " + where_clause

        if start_position:
            start_position = " STARTPOSITION " + str(start_position)

        if max_results:
            max_results = " MAXRESULTS " + str(max_results)

        select = "SELECT * FROM {0} {1}{2}{3}".format(cls.qbo_object_name, where_clause, start_position, max_results)

        return cls.query(select, qb=qb)

    @classmethod
    def query(cls, select, qb=None):
        """
        :param select: QBO SQL query select statement
        :return: Returns list
        """
        if not qb:
            qb = QuickBooks()

        json_data = qb.query(select)

        obj_list = []

        if cls.qbo_object_name in json_data["QueryResponse"]:
            for item_json in json_data["QueryResponse"][cls.qbo_object_name]:
                obj_list.append(cls.from_json(item_json))

        return obj_list


class QuickbooksPdfDownloadable(object):
    qbo_object_name = ""

    def download_pdf(self):
        if self.Id and self.Id > 0:
            qb = QuickBooks()
            return qb.download_pdf(self.qbo_object_name, self.Id)
        else:
            raise QuickbooksException("Cannot download {0} when no Id is assigned".format(self.qbo_object_name))
