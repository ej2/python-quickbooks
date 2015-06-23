from base import QuickbooksBaseObject, Ref


'''
QBO definition: Tax Agency is an entity that is associated with a tax rate and identifies the agency to which that tax rate
applies, that is, the entity that collects those taxes.
'''
class TaxAgency(QuickbooksBaseObject):
    class_dict = {}

    qbo_object_name = "TaxAgency"

    DisplayName = ""
    TaxTrackedOnSales = True
    TaxTrackedOnPurchases = False

    def __unicode__(self):
        return self.DisplayName
