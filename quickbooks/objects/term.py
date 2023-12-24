from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class Term(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Term entity represents the terms under which a sale is made, typically expressed in the
    form of days due after the goods are received. Optionally, a discount of the total amount may be applied if
    payment is made within a stipulated time. For example, net 30 indicates that payment is due within 30 days.
    A term of 2%/15 net 60 indicates that payment is due within 60 days, with a discount of 2% if payment is made
    within 15 days. This entity also supports: -An absolute due date -A number of days from a start
    date -A percent discount -An absolute discount
    """

    qbo_object_name = "Term"

    def __init__(self):
        super(Term, self).__init__()
        self.Name = ""
        self.Active = True
        self.Type = None  # Readonly
        self.DiscountPercent = None
        self.DueDays = None
        self.DiscountDays = None
        self.DayOfMonthDue = None
        self.DueNextMonthDays = None
        self.DiscountDayOfMonth = None

    def __str__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()

        ref.name = self.Name
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
