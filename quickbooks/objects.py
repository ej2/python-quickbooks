from mixins import ToJsonMixin, FromJsonMixin, ReadMixin, CreateMixin, ListMixin, UpdateMixin


class QuickbooksBaseObject():
    SyncToken = 0
    sparse = "false"


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


class TaxCodeRef(ToJsonMixin, FromJsonMixin):
    def __init__(self):
        self.value = ""

    def __unicode__(self):
        return self.value

class Customer(QuickbooksBaseObject, ToJsonMixin, FromJsonMixin, ReadMixin, CreateMixin, ListMixin, UpdateMixin):
    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "PrimaryPhone": PhoneNumber,
        "Mobile": PhoneNumber,
        "Fax": PhoneNumber,
        "PrimaryEmailAddr": EmailAddress,
        "WebAddr": WebAddress,
        "DefaultTaxCodeRef": TaxCodeRef
    }

    qbo_object_name = "Customer"

    Title = ""
    GivenName = ""
    MiddleName = ""
    FamilyName = ""
    Suffix = ""
    FullyQualifiedName = ""
    CompanyName = ""
    DisplayName = ""
    PrintOnCheckName = ""
    Notes = ""
    Active = ""

    BillAddr = None
    ShipAddr = None
    PrimaryPhone = None
    Mobile = None
    Fax = None
    PrimaryEmailAddr = None
    WebAddr = None
    DefaultTaxCodeRef = None

    def __unicode__(self):
        return self.DisplayName


    # "Taxable": false,
    # "Job": false,
    # "BillWithParent": false,
    # "Balance": 85.0,
    # "BalanceWithJobs": 85.0,
    # "PreferredDeliveryMethod": "Print",
    # "domain": "QBO",
    # "Id": "2",
    # "MetaData": {
    #     "CreateTime": "2014-12-03T16:49:28-08:00",
    #     "LastUpdatedTime": "2014-12-10T12:56:01-08:00"
    # },
    # "PrintOnCheckName": "Bill's Windsurf Shop",
    # "Active": true,
    #