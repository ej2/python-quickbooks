from base import Ref, QuickbooksManagedObject, LinkedTxnMixin


class TimeActivity(QuickbooksManagedObject, LinkedTxnMixin):
    """
    QBO definition: The TimeActivity entity represents a record of time worked by a vendor or employee.
    """
    class_dict = {
        "VendorRef": Ref,
        "CustomerRef": Ref,
        "DepartmentRef": Ref,
        "ItemRef": Ref,
        "ClassRef": Ref,
    }

    qbo_object_name = "TimeActivity"

    def __init__(self):
        super(TimeActivity, self).__init__()
        self.NameOf = ""
        self.BillableStatus = ""
        self.Taxable = ""
        self.HourlyRate = ""
        self.BreakHours = ""
        self.BreakMinutes = ""
        self.StartTime = ""
        self.EndTime = ""
        self.Description = ""

        self.VendorRef = None
        self.CustomerRef = None
        self.DepartmentRef = None
        self.ItemRef = None
        self.ClassRef = None
