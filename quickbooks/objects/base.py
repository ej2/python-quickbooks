from ..mixins import ToJsonMixin, FromJsonMixin, ReadMixin, ListMixin, UpdateMixin


class QuickbooksBaseObject(ToJsonMixin, FromJsonMixin, ReadMixin, ListMixin, UpdateMixin):
    class_dict = {}
    list_dict = {}

    Id = 0
    SyncToken = 0
    sparse = "false"
    domain = "QBO"


class MetaData:
    def __init__(self):
        self.CreateTime = ""
        self.LastUpdatedTime = ""


class Address(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.Id = 0
        self.Line1 = ""
        self.Line2 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.PostalCode = ""

    def __unicode__(self):
        return "{0} {1}, {2} {3}".format(self.Line1, self.City, self.CountrySubDivisionCode, self.PostalCode)


class PhoneNumber(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.FreeFormNumber = ""

    def __unicode__(self):
        return self.FreeFormNumber


class EmailAddress(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.Address = ""

    def __unicode__(self):
        return self.Address


class WebAddress(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

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

    def __unicode__(self):
        return self.name


class CustomField(ToJsonMixin, FromJsonMixin):
    class_dict = {}
    list_dict = {}

    def __init__(self):
        self.Type = ""
        self.Name = ""
        self.StringValue = ""

    def __unicode__(self):
        return self.Name


class LinkedTxn(QuickbooksBaseObject):
    class_dict = {}
    list_dict = {}

    qbo_object_name = "LinkedTxn"

    def __init__(self):
        self.TxnId = 0
        self.TxnType = 0
        self.TxnLineId = 0


class CustomerMemo(QuickbooksBaseObject):
    def __init__(self):
        self.Value = ""

    def __unicode__(self):
        return self.Value
