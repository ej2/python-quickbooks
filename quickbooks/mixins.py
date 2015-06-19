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


class ReadMixin:
    qbo_object_name = ""

    @classmethod
    def get(cls, id):
        from client import QuickBooks
        qb = QuickBooks()

        json_data = qb.get_single_object(cls.qbo_object_name, pk=id)
        obj = cls()
        obj.from_json(json_data[cls.qbo_object_name])

        return obj


class CreateMixin:
    qbo_object_name = ""

    @classmethod
    def create(cls):
        from client import QuickBooks
        qb = QuickBooks()

        json_data = qb.create_object(cls.qbo_object_name, cls.to_json())

        obj = cls()
        obj.from_json(json_data[cls.qbo_object_name])

        return obj


class ListMixin:
    qbo_object_name = ""

    @classmethod
    def all(cls):
        from client import QuickBooks

        qb = QuickBooks()

        json_data = qb.get_all(cls.qbo_object_name)

        obj_list = []
        for item_json in json_data[cls.qbo_object_name]:
            obj = cls()
            obj_list.append(obj.from_json(item_json))

        return obj_list

    @classmethod
    def filter(cls, query):
        from client import QuickBooks
        qb = QuickBooks()

        json_data = qb.get_list(cls.qbo_object_name, query)

        list = []
        for item_json in json_data[cls.qbo_object_name]:
            obj = cls()
            list.append(obj.from_json(item_json))

        return list
