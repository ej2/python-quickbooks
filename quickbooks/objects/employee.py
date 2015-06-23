from base import QuickbooksBaseObject, Address, PhoneNumber, Ref


'''
QBO definition: Employee represents the people who are working for the company.
'''
class Employee(QuickbooksBaseObject):
    class_dict = {
        "PrimaryAddr": Address,
        "PrimaryPhone": PhoneNumber
    }

    qbo_object_name = "Employee"

    def __init__(self):
        self.SSN = ""
        self.BillableTime = ""
        self.GivenName = ""
        self.FamilyName = ""
        self.DisplayName = ""
        self.PrintOnCheckName = ""
        self.Active = True

        self.PrimaryAddr = None

    def __unicode__(self):
        return self.DisplayName
