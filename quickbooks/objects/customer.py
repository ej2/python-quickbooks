from base import QuickbooksBaseObject, Address, PhoneNumber, EmailAddress, WebAddress, Ref


'''
QBO definition: A customer is a consumer of the service or product that your business offers. The Customer object allows you
to categorize customers according to your business requirements. You must first create a customer and then
create a job referencing that customer as a parent with the ParentRef attribute. Some areas a sub-customer/job
can be used include:

  -To track a job for the top-level customer, such as a kitchen remodel or bathroom remodel.
  -Members of a team or league.
  -Properties managed by a Homeowner Association or Property Management Company.
'''
class Customer(QuickbooksBaseObject):
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
        "PaymentMethodRef": Ref
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
    Active = True
    Job = False
    BillWithParent = False
    Taxable = True
    Balance = 0
    BalanceWithJobs = 0
    PreferredDeliveryMethod = ""
    ResaleNum = ""

    BillAddr = None
    ShipAddr = None
    PrimaryPhone = None
    Mobile = None
    Fax = None
    PrimaryEmailAddr = None
    WebAddr = None
    DefaultTaxCodeRef = None
    SalesTermRef = None
    PaymentMethodRef = None

    def __unicode__(self):
        return self.DisplayName
