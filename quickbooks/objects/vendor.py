from base import Address, PhoneNumber, EmailAddress, WebAddress, Ref, QuickbooksManagedObject


class Vendor(QuickbooksManagedObject):
    """
    QBO definition: The Vendor represents the seller from whom your company purchases any service or product.
    """

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

    def __init__(self):
        super(Vendor, self).__init__()
        self.Title = ""
        self.GivenName = ""
        self.FamilyName = ""
        self.Suffix = ""
        self.CompanyName = ""
        self.DisplayName = ""
        self.PrintOnCheckName = ""
        self.Active = True
        self.TaxIdentifier = 0
        self.Balance = 0
        self.AcctNum = ""
        self.Vendor1099 = True

        self.BillAddr = None
        self.PrimaryPhone = None
        self.Mobile = None
        self.Fax = None
        self.PrimaryEmailAddr = None
        self.WebAddr = None
        self.TermRef = None

    def __unicode__(self):
        return self.DisplayName

    def to_ref(self):
        ref = Ref()

        ref.name = self.DisplayName
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref