from base import QuickbooksBaseObject, Address, PhoneNumber, EmailAddress, WebAddress, Ref


'''
QBO definition: The Vendor represents the seller from whom your company purchases any service or product.
'''
class Vendor(QuickbooksBaseObject):
    class_dict = {
        "BillAddr": Address,
        "TermRef": Ref,
        "PrimaryPhone": PhoneNumber,
        "Mobile": PhoneNumber,
        "Fax": PhoneNumber,
        "PrimaryEmailAddr": EmailAddress,
        "WebAddr": WebAddress,
    }

    qbo_object_name = "Vendor"

    Title = ""
    GivenName = ""
    FamilyName = ""
    Suffix = ""
    CompanyName = ""
    DisplayName = ""
    PrintOnCheckName = ""
    Active = True
    TaxIdentifier = 0
    Balance = 0
    AcctNum = ""
    Vendor1099 = True

    BillAddr = None
    PrimaryPhone = None
    Mobile = None
    Fax = None
    PrimaryEmailAddr = None
    WebAddr = None
    TermRef = None

    def __unicode__(self):
        return self.DisplayName
