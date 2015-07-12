import json


class ToJsonMixin(object):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FromJsonMixin(object):
    class_dict = {}

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
    def get(cls, id):
        from client import QuickBooks
        qb = QuickBooks()

        json_data = qb.get_single_object(cls.qbo_object_name, pk=id)
        return cls.from_json(json_data[cls.qbo_object_name])


class UpdateMixin(object):
    qbo_object_name = ""

    def save(self):
        from client import QuickBooks
        qb = QuickBooks()

        if self.Id > 0:
            json_data = qb.update_object(self.qbo_object_name, self.to_json())
        else:
            json_data = qb.create_object(self.qbo_object_name, self.to_json())

        obj = type(self).from_json(json_data[self.qbo_object_name])
        self.Id = obj.Id

        return obj


class ListMixin(object):
    qbo_object_name = ""

    @classmethod
    def all(cls):
        from client import QuickBooks

        qb = QuickBooks()

        json_data = qb.get_all(cls.qbo_object_name)

        obj_list = []
        for item_json in json_data["QueryResponse"][cls.qbo_object_name]:
            obj_list.append(cls.from_json(item_json))

        return obj_list

    @classmethod
    def filter(cls, **kwargs):
        from client import QuickBooks
        qb = QuickBooks()

        json_data = qb.get_list(cls.qbo_object_name, **kwargs)

        obj_list = []
        for item_json in json_data["QueryResponse"][cls.qbo_object_name]:
            obj_list.append(cls.from_json(item_json))

        return obj_list
