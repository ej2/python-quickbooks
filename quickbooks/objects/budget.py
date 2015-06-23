from base import QuickbooksBaseObject, Ref


'''
QBO definition: The Budget endpoint allows you to retrieve the current state of budgets already set up in the user's
company file. A budget allows for an amount to be assigned on a monthly, quarterly, or annual basis for a specific
account or customer and are created to give a business measurable expense goals. This amount represents how much
should be spent against that account or customer in the give time period.
'''
class Budget(QuickbooksBaseObject):
    class_dict = {
        "BudgetDetail": BudgetDetail,
    }

    qbo_object_name = "Budget"

    Name = ""
    StartDate = ""
    EndDate = ""
    BudgetType = ""
    BudgetEntryType = ""
    Active = True

    BudgetDetail = None

    def __unicode__(self):
        return self.Name


class BudgetDetail(QuickbooksBaseObject, ToJsonMixin, FromJsonMixin):
    class_dict = {
        "AccountRef": Ref,
        "CustomerRef": Ref
    }

    BudgetDate = ""
    Amount = 0

    AccountRef = None
    CustomerRef = None

    def __unicode__(self):
        return self.Amount