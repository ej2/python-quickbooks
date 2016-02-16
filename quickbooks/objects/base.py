from six import python_2_unicode_compatible
from ..mixins import ToJsonMixin, FromJsonMixin, ReadMixin, ListMixin, UpdateMixin


class QuickbooksBaseObject(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}


class QuickbooksTransactionEntity(QuickbooksBaseObject):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.Id = None
        self.SyncToken = 0
        self.sparse = False
        self.domain = "QBO"


class QuickbooksManagedObject(QuickbooksBaseObject, ReadMixin, ListMixin, UpdateMixin):
    pass


class QuickbooksReadOnlyObject(QuickbooksBaseObject, ReadMixin, ListMixin):
    pass


@python_2_unicode_compatible
class MetaData:
    def __init__(self):
        self.CreateTime = ""
        self.LastUpdatedTime = ""

    def __str__(self):
        return "Created {0}".format(self.CreateTime)


class LinkedTxnMixin(object):
    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = self.qbo_object_name
        linked_txn.TxnLineId = 1

        return linked_txn


@python_2_unicode_compatible
class Address(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Id = None
        self.Line1 = ""
        self.Line2 = ""
        self.Line3 = ""
        self.Line4 = ""
        self.Line5 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.Country = ""
        self.PostalCode = ""
        self.Lat = ""
        self.Long = ""
        self.Note = ""

    def __str__(self):
        return "{0} {1}, {2} {3}".format(self.Line1, self.City, self.CountrySubDivisionCode, self.PostalCode)


@python_2_unicode_compatible
class PhoneNumber(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.FreeFormNumber = ""

    def __str__(self):
        return self.FreeFormNumber


@python_2_unicode_compatible
class EmailAddress(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Address = ""

    def __str__(self):
        return self.Address


@python_2_unicode_compatible
class WebAddress(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.URI = ""

    def __str__(self):
        return self.URI


@python_2_unicode_compatible
class Ref(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.value = ""
        self.name = ""
        self.type = ""

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CustomField(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Type = ""
        self.Name = ""
        self.StringValue = ""

    def __str__(self):
        return self.Name


@python_2_unicode_compatible
class LinkedTxn(QuickbooksBaseObject):
    qbo_object_name = "LinkedTxn"

    def __init__(self):
        super(LinkedTxn, self).__init__()
        self.TxnId = 0
        self.TxnType = 0
        self.TxnLineId = 0

    def __str__(self):
        return str(self.TxnId)


@python_2_unicode_compatible
class CustomerMemo(QuickbooksBaseObject):
    def __init__(self):
        super(CustomerMemo, self).__init__()
        self.value = ""

    def __str__(self):
        return self.value


class MarkupInfo(QuickbooksBaseObject):
    class_dict = {
        "PriceLevelRef": Ref,
    }

    def __init__(self):
        super(MarkupInfo, self).__init__()
        self.PercentBased = False
        self.Value = 0
        self.Percent = 0
        self.PriceLevelRef = None


class AttachableRef(QuickbooksBaseObject):
    class_dict = {
        "EntityRef": Ref
    }

    list_dict = {
        "CustomField": CustomField
    }

    qbo_object_name = "AttachableRef"

    def __init__(self):
        super(AttachableRef, self).__init__()

        self.LineInfo = ""
        self.IncludeOnSend = False
        self.Inactive = False
        self.NoRefOnly = False

        self.EntityRef = None
        self.CustomField = []
