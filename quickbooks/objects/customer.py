from six import python_2_unicode_compatible
from .base import Address, PhoneNumber, EmailAddress, WebAddress, Ref, QuickbooksManagedObject, \
    QuickbooksTransactionEntity


@python_2_unicode_compatible
class Customer(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: A customer is a consumer of the service or product that your business offers. The Customer object
    allows you to categorize customers according to your business requirements. You must first create a customer
    and then create a job referencing that customer as a parent with the ParentRef attribute. Some areas a
    sub-customer/job can be used include:

      -To track a job for the top-level customer, such as a kitchen remodel or bathroom remodel.
      -Members of a team or league.
      -Properties managed by a Homeowner Association or Property Management Company.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "PrimaryPhone": PhoneNumber,
        "AlternatePhone": PhoneNumber,
        "Mobile": PhoneNumber,
        "Fax": PhoneNumber,
        "PrimaryEmailAddr": EmailAddress,
        "WebAddr": WebAddress,
        "DefaultTaxCodeRef": Ref,
        "SalesTermRef": Ref,
        "PaymentMethodRef": Ref,
        "CurrencyRef": Ref,
        "ParentRef": Ref,
        "ARAccountRef": Ref,
    }

    qbo_object_name = "Customer"

    def __init__(self):
        super(Customer, self).__init__()
        self.Title = ""
        self.GivenName = ""
        self.MiddleName = ""
        self.FamilyName = ""
        self.Suffix = ""
        self.FullyQualifiedName = ""
        self.CompanyName = ""
        self.DisplayName = ""  # Constraints:Must be unique
        self.PrintOnCheckName = ""
        self.Notes = ""
        self.Active = True
        self.Job = False
        self.BillWithParent = False
        self.Taxable = True
        self.Balance = 0
        self.BalanceWithJobs = 0
        self.PreferredDeliveryMethod = ""
        self.ResaleNum = ""
        self.Level = 0
        self.OpenBalanceDate = ""

        self.BillAddr = None
        self.ShipAddr = None
        self.PrimaryPhone = None
        self.AlternatePhone = None
        self.Mobile = None
        self.Fax = None
        self.PrimaryEmailAddr = None
        self.WebAddr = None
        self.DefaultTaxCodeRef = None
        self.SalesTermRef = None
        self.PaymentMethodRef = None
        self.ParentRef = None
        self.ARAccountRef = None

    def __str__(self):
        return self.DisplayName

    def to_ref(self):
        ref = Ref()

        ref.name = self.DisplayName
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
