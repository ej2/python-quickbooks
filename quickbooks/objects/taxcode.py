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

    Name = ""
    Description = ""
    Taxable = True
    TaxGroup = True
    Active = True

    SalesTaxRateList = None
    PurchaseTaxRateList = None

    def __unicode__(self):
        return self.Name


#TODO: make to_json and from_json work with lists
class TaxRateList(QuickbooksBaseObject):
    class_dict = {}
    qbo_object_name = "TaxRateList"

    TaxRateDetail = []


class TaxRateDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxRateRef": Ref
    }

    qbo_object_name = "TaxRateDetail"

    TaxTypeApplicable = ""
    TaxOrder = 0
    TaxRateRef = None
