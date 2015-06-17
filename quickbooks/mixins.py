import json


class ToJsonMixin(object):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FromJsonMixin(object):
    class_dict = {}

    def from_json(self, json_data):
        for key in json_data:
            if key in self.class_dict:
                obj = self.class_dict[key]()
                obj.from_json(json_data[key])
                setattr(self, key, obj)
            else:
                setattr(self, key, json_data[key])



class QuickBooksManagerMixin:
    qbo_object_name = ""
    qbo_object_class = None

    def __init__(self, client):
        self.client = client

    def get(self, id):
        json_data = self.client.get_single_object(self.qbo_object_name, pk=id)
        obj = self.qbo_object_class()
        obj.from_json(json_data[self.qbo_object_name])

        return obj


class ReadMixin:
    qbo_object_name = ""

    @classmethod
    def get(cls, id):
        from quickbooks import QuickBooks
        qb = QuickBooks()

        json_data = qb.get_single_object(cls.qbo_object_name, pk=id)
        obj = cls()
        obj.from_json(json_data[cls.qbo_object_name])

        return obj

class CreateMixin:
    qbo_object_name = ""

    def create(self):
        from quickbooks import QuickBooks
        qb = QuickBooks()

        return qb.create_object(self.qbo_object_name, self.to_json())
