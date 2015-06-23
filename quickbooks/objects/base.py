from ..mixins import ToJsonMixin, FromJsonMixin, ReadMixin, CreateMixin, ListMixin, UpdateMixin


class QuickbooksBaseObject(ToJsonMixin, FromJsonMixin, ReadMixin, CreateMixin, ListMixin, UpdateMixin):
    Id = 0
    SyncToken = 0
    sparse = "false"
    domain = "QBO"


class MetaData:
    def __init__(self):
        self.CreateTime = ""
        self.LastUpdatedTime = ""


class Address(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.Id = 0
        self.Line1 = ""
        self.Line2 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.PostalCode = ""

    def __unicode__(self):
        return "{} {}, {} {}".format(self.Line1, self.City, self.CountrySubDivisionCode, self.PostalCode)


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
    def __init__(self):
        self.value = ""
        self.name = ""

    def __unicode__(self):
        return self.name

