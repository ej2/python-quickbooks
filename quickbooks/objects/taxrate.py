from base import QuickbooksManagedObject


class TaxRate(QuickbooksManagedObject):
    """
    QBO definition: A TaxRate object represents rate applied to calculate tax liability. Use the TaxService
    entity to create a taxrate.
    """
    class_dict = {}

    qbo_object_name = "TaxRate"

    def __init__(self):
        super(TaxRate, self).__init__()
        self.Name = ""
        self.Description = ""
        self.RateValue = 0
        self.SpecialTaxType = ""
        self.Active = True

        self.AgencyRef = None
        self.TaxReturnLineRef = None

    def __unicode__(self):
        return self.Name


