from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref, CustomField, MetaData


class CompanyCurrency(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Applicable only for those companies that enable multicurrency, a companycurrency object
    defines a currency that is active in the QuickBooks Online company. One or more companycurrency objects
    are active based on the company's multicurrency business requirements and correspond to the list
    displayed by the Currency Center in the QuickBooks Online UI
    """

    class_dict = {
        "CustomField": CustomField,
        "MetaData": MetaData,
    }

    qbo_object_name = "CompanyCurrency"

    def __init__(self):
        super(CompanyCurrency, self).__init__()

        self.Id = None
        self.Code = ""
        self.Name = ""
        self.Active = True

        self.CustomField = None
        self.MetaData = None

    def __str__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()

        ref.name = self.Name
        ref.type = self.qbo_object_name
        ref.value = self.Code

        return ref
