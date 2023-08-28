from ..mixins import ToJsonMixin, FromJsonMixin


class BatchOperation(object):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class FaultError(FromJsonMixin):
    qbo_object_name = "Error"

    def __init__(self):
        super(FaultError, self).__init__()

        self.Message = ""
        self.code = ""
        self.Detail = ""
        self.element = ""

    def __str__(self):
        return "Code: {0} Message: {1} Detail: {2}".format(self.code, self.Message, self.Detail)

    def __repr__(self):
        return self.__str__()


class Fault(FromJsonMixin):
    list_dict = {
        "Error": FaultError
    }

    qbo_object_name = "Fault"

    def __init__(self):
        super(Fault, self).__init__()

        self.type = ""
        self.original_object = None
        self.Error = []

    def __repr__(self):
        return "{0} Errors".format(len(self.Error))


class BatchItemResponse(FromJsonMixin):
    qbo_object_name = "BatchItemResponse"

    def __init__(self):
        super(BatchItemResponse, self).__init__()
        self.bId = ""
        self.list_dict = {}
        self.class_dict = {
            "Fault": Fault
        }

        self._original_object = None
        self.Fault = None

    def set_object(self, obj):
        self.class_dict[obj.qbo_object_name] = obj
        setattr(self, obj.qbo_object_name, obj)
        self._original_object = obj

    def get_object(self):
        return self._original_object


class BatchResponse(object):

    def __init__(self):
        self.batch_responses = []
        self.original_list = []
        self.successes = []
        self.faults = []


class BatchItemRequest(ToJsonMixin):
    class_dict = {}
    list_dict = {}

    qbo_object_name = "BatchItemRequest"

    def __init__(self):
        self.bId = ""
        self.operation = ""
        self._original_object = None

    def set_object(self, obj):
        self.class_dict[obj.qbo_object_name] = obj
        setattr(self, obj.qbo_object_name, obj)
        self._original_object = obj

    def get_object(self):
        return self._original_object


class IntuitBatchRequest(ToJsonMixin):
    list_dict = {
        "BatchItemRequest": BatchItemRequest
    }

    def __init__(self):
        self.BatchItemRequest = []
