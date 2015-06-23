from base import QuickbooksBaseObject


'''
QBO definition: A TaxRate object represents rate applied to calculate tax liability. Use the TaxService
entity to create a taxrate.
'''
class TaxRate(QuickbooksBaseObject):
    class_dict = {}

    qbo_object_name = "TaxRate"

    Name = ""
    Description = ""
    RateValue = 0
    SpecialTaxType = ""
    Active = True

    AgencyRef = None
    TaxReturnLineRef = None

    def __unicode__(self):
        return self.Name


