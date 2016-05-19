from six import python_2_unicode_compatible
from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


@python_2_unicode_compatible
class TaxRate(QuickbooksManagedObject, QuickbooksTransactionEntity):
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


