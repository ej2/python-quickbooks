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

    SSN = ""
    BillableTime = ""
    GivenName = ""
    FamilyName = ""
    DisplayName = ""
    PrintOnCheckName = ""
    Active = True

    PrimaryAddr = None

    def __unicode__(self):
        return self.DisplayName
