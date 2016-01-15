from six import python_2_unicode_compatible
from .base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, AttachableRef


@python_2_unicode_compatible
class TimeActivity(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The TimeActivity entity represents a record of time worked by a vendor or employee.
    """
    class_dict = {
        "VendorRef": Ref,
        "CustomerRef": Ref,
        "DepartmentRef": Ref,
        "EmployeeRef": Ref,
        "ItemRef": Ref,
        "ClassRef": Ref,
        "AttachableRef": AttachableRef
    }

    qbo_object_name = "TimeActivity"

    def __init__(self):
        super(TimeActivity, self).__init__()
        self.NameOf = ""
        self.TimeZone = ""
        self.TxnDate = ""
        self.BillableStatus = ""
        self.Taxable = False
        self.HourlyRate = 0
        self.Hours = 0
        self.Minutes = 0
        self.BreakHours = 0
        self.BreakMinutes = 0
        self.StartTime = ""
        self.EndTime = ""
        self.Description = ""

        self.VendorRef = None
        self.CustomerRef = None
        self.DepartmentRef = None
        self.EmployeeRef = None
        self.ItemRef = None
        self.ClassRef = None
        self.AttachableRef = None

    def __str__(self):
        return self.NameOf
