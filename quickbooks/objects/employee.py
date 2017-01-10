from six import python_2_unicode_compatible
from .base import Address, PhoneNumber, QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


@python_2_unicode_compatible
class Employee(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Employee represents the people who are working for the company.
    """

    class_dict = {
        "PrimaryAddr": Address,
        "PrimaryPhone": PhoneNumber
    }

    qbo_object_name = "Employee"

    def __init__(self):
        super(Employee, self).__init__()
        self.SSN = ""

        self.GivenName = ""
        self.FamilyName = ""
        self.MiddleName = ""
        self.DisplayName = ""
        self.Suffix = ""
        self.PrintOnCheckName = ""
        self.EmployeeNumber = ""
        self.Title = ""
        self.BillRate = 0
        self.BirthDate = ""
        self.Gender = None
        self.HiredDate = ""
        self.ReleasedDate = ""
        self.Active = True
        self.Organization = False
        self.BillableTime = False

        self.PrimaryAddr = None

    def __str__(self):
        return self.DisplayName

    def to_ref(self):
        ref = Ref()

        ref.name = self.DisplayName
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
