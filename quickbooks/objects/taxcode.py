from base import QuickbooksBaseObject, Ref


'''
QBO definition: The PaymentMethod entity provides the method of payment for received goods. Delete is achieved by setting the
Active attribute to false in an entity update request; thus, making it inactive. In this type of delete,
the record is not permanently deleted, but is hidden for display purposes. References to inactive objects are
left intact.
'''
class TaxCode(QuickbooksBaseObject):
    class_dict = {
        "SalesTaxRateList": TaxRateList,
        "PurchaseTaxRateList": TaxRateList,
    }

    qbo_object_name = "TaxCode"

    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Taxable = True
        self.TaxGroup = True
        self.Active = True

        self.SalesTaxRateList = None
        self.PurchaseTaxRateList = None

    def __unicode__(self):
        return self.Name


#TODO: make to_json and from_json work with lists
class TaxRateList(QuickbooksBaseObject):
    class_dict = {}
    qbo_object_name = "TaxRateList"

    def __init__(self):
        self.TaxRateDetail = []


class TaxRateDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxRateRef": Ref
    }

    qbo_object_name = "TaxRateDetail"

    def __init__(self):
        self.TaxTypeApplicable = ""
        self.TaxOrder = 0
        self.TaxRateRef = None
