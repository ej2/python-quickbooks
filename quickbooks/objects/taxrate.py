from base import QuickbooksBaseObject


'''
QBO definition: A TaxRate object represents rate applied to calculate tax liability. Use the TaxService
entity to create a taxrate.
'''
class TaxRate(QuickbooksBaseObject):
    class_dict = {}

    qbo_object_name = "TaxRate"

    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.RateValue = 0
        self.SpecialTaxType = ""
        self.Active = True

        self.AgencyRef = None
        self.TaxReturnLineRef = None

    def __unicode__(self):
        return self.Name


