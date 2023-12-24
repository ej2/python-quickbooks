from .base import QuickbooksBaseObject, Ref, QuickbooksTransactionEntity, \
    QuickbooksReadOnlyObject


class BudgetDetail(QuickbooksBaseObject):
    class_dict = {
        "AccountRef": Ref,
        "CustomerRef": Ref,
        "ClassRef": Ref,
        "DepartmentRef": Ref,
    }

    def __init__(self):
        super(BudgetDetail, self).__init__()
        self.BudgetDate = ""
        self.Amount = 0

        self.AccountRef = None
        self.CustomerRef = None
        self.ClassRef = None
        self.DepartmentRef = None

    def __str__(self):
        return str(self.Amount)


class Budget(QuickbooksReadOnlyObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Budget endpoint allows you to retrieve the current state of budgets already set up in the user's
    company file. A budget allows for an amount to be assigned on a monthly, quarterly, or annual basis for a specific
    account or customer and are created to give a business measurable expense goals. This amount represents how much
    should be spent against that account or customer in the give time period.

    Note: Budgets cannot be created or updated via the Quickbooks API
    """

    list_dict = {
        "BudgetDetail": BudgetDetail,
    }

    qbo_object_name = "Budget"

    def __init__(self):
        super(Budget, self).__init__()
        self.Name = ""
        self.StartDate = ""
        self.EndDate = ""
        self.BudgetType = ""
        self.BudgetEntryType = ""
        self.Active = True

        self.BudgetDetail = []

    def __str__(self):
        return self.Name
