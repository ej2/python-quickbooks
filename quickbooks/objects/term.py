from six import python_2_unicode_compatible
from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, AttachableRef


@python_2_unicode_compatible
class Term(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Term entity represents the terms under which a sale is made, typically expressed in the
    form of days due after the goods are received. Optionally, a discount of the total amount may be applied if
    payment is made within a stipulated time. For example, net 30 indicates that payment is due within 30 days.
    A term of 2%/15 net 60 indicates that payment is due within 60 days, with a discount of 2% if payment is made
    within 15 days. This entity also supports: -An absolute due date -A number of days from a start
    date -A percent discount -An absolute discount
    """

    class_dict = {
        "AttachableRef": AttachableRef
    }
    qbo_object_name = "Term"

    def __init__(self):
        super(Term, self).__init__()
        self.Name = ""
        self.Type = ""
        self.DiscountPercent = 0
        self.DueDays = 0
        self.DayOfMonthDue = 0
        self.DueNextMonthDays = 0
        self.DiscountDays = 0
        self.DiscountDayOfMonth = 0
        self.Active = True

        self.AttachableRef = None

    def __str__(self):
        return self.Name
