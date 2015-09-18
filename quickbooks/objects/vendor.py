from six import python_2_unicode_compatible
from .base import Address, PhoneNumber, EmailAddress, WebAddress, Ref, QuickbooksBaseObject, \
    QuickbooksManagedObject, QuickbooksTransactionEntity


class ContactInfo(QuickbooksBaseObject):
    class_dict = {
        "Telephone": PhoneNumber
    }

    def __init__(self):
        super(ContactInfo, self).__init__()

        self.Type = ""
        self.Telephone = None


@python_2_unicode_compatible
class Vendor(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Vendor represents the seller from whom your company purchases any service or product.
    """

    class_dict = {
        "BillAddr": Address,
        "TermRef": Ref,
        "PrimaryPhone": PhoneNumber,
        "AlternatePhone": PhoneNumber,
        "Mobile": PhoneNumber,
        "Fax": PhoneNumber,
        "PrimaryEmailAddr": EmailAddress,
        "WebAddr": WebAddress,
        "CurrencyRef": Ref,
        "APAccountRef": Ref
    }

    qbo_object_name = "Vendor"

    def __init__(self):
        super(Vendor, self).__init__()
        self.Title = ""
        self.GivenName = ""
        self.MiddleName = ""
        self.FamilyName = ""
        self.Suffix = ""
        self.CompanyName = ""
        self.DisplayName = ""
        self.PrintOnCheckName = ""
        self.Active = True
        self.TaxIdentifier = ""
        self.Balance = 0
        self.AcctNum = ""
        self.Vendor1099 = True
        self.TaxReportingBasis = ""

        self.BillAddr = None
        self.PrimaryPhone = None
        self.AlternatePhone = None
        self.Mobile = None
        self.Fax = None
        self.PrimaryEmailAddr = None
        self.WebAddr = None
        self.TermRef = None
        self.CurrencyRef = None
        self.APAccountRef = None

    def __str__(self):
        return self.DisplayName

    def to_ref(self):
        ref = Ref()

        ref.name = self.DisplayName
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
