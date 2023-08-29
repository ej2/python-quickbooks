from quickbooks.mixins import ListMixin, ReadMixin
from .base import QuickbooksTransactionEntity, Ref, QuickbooksBaseObject


class TaxRate(QuickbooksTransactionEntity, QuickbooksBaseObject, ReadMixin, ListMixin):
    """
    QBO definition: A TaxRate object represents rate applied to calculate tax liability. Use the TaxService
    entity to create a taxrate.
    """
    class_dict = {
        "AgencyRef": Ref,
        "TaxReturnLineRef": Ref,
    }

    qbo_object_name = "TaxRate"

    def __init__(self):
        super(TaxRate, self).__init__()

        # All values are readonly - TaxRates cannot be created or modified with the TaxRate object
        self.Name = ""
        self.Description = ""
        self.RateValue = 0
        self.SpecialTaxType = ""
        self.Active = True
        self.DisplayType = ""
        self.EffectiveTaxRate = ""

        self.AgencyRef = None
        self.TaxReturnLineRef = None

    def __str__(self):
        return self.Name
