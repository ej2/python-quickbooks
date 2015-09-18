from six import python_2_unicode_compatible
from .base import QuickbooksTransactionEntity, QuickbooksManagedObject


@python_2_unicode_compatible
class TaxAgency(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Tax Agency is an entity that is associated with a tax rate and identifies the agency to which that tax rate
    applies, that is, the entity that collects those taxes.
    """

    class_dict = {}

    qbo_object_name = "TaxAgency"

    def __init__(self):
        super(TaxAgency, self).__init__()
        self.DisplayName = ""
        self.TaxRegistrationNumber = ""
        self.TaxTrackedOnSales = True
        self.TaxTrackedOnPurchases = False

    def __str__(self):
        return self.DisplayName
