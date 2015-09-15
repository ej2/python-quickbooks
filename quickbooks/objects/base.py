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
        self.TxnDate = ""


class QuickbooksManagedObject(QuickbooksBaseObject, ReadMixin, ListMixin, UpdateMixin):
    pass


class MetaData:
    def __init__(self):
        self.CreateTime = ""
        self.LastUpdatedTime = ""

    def __unicode__(self):
        return "Created {0}".format(self.CreateTime)


class LinkedTxnMixin(object):
    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = self.qbo_object_name
        linked_txn.TxnLineId = 1

        return linked_txn


class Address(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Id = None
        self.Line1 = ""
        self.Line2 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.PostalCode = ""
        self.Lat = ""
        self.Long = ""

    def __unicode__(self):
        return "{0} {1}, {2} {3}".format(self.Line1, self.City, self.CountrySubDivisionCode, self.PostalCode)


class PhoneNumber(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.FreeFormNumber = ""

    def __unicode__(self):
        return self.FreeFormNumber


class EmailAddress(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Address = ""

    def __unicode__(self):
        return self.Address


class WebAddress(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.URI = ""

    def __unicode__(self):
        return self.URI


class Ref(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.value = ""
        self.name = ""
        self.type = ""

    def __unicode__(self):
        return self.name


class CustomField(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Type = ""
        self.Name = ""
        self.StringValue = ""

    def __unicode__(self):
        return self.Name


class LinkedTxn(QuickbooksBaseObject):
    qbo_object_name = "LinkedTxn"

    def __init__(self):
        super(LinkedTxn, self).__init__()
        self.TxnId = 0
        self.TxnType = 0
        self.TxnLineId = 0

    def __unicode__(self):
        return str(self.TxnId)


class CustomerMemo(QuickbooksBaseObject):
    def __init__(self):
        super(CustomerMemo, self).__init__()
        self.Value = ""

    def __unicode__(self):
        return self.Value


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
