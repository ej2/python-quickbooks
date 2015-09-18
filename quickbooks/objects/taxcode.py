from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, QuickbooksTransactionEntity


class TaxRateDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxRateRef": Ref
    }

    qbo_object_name = "TaxRateDetail"

    def __init__(self):
        super(TaxRateDetail, self).__init__()
        self.TaxTypeApplicable = ""
        self.TaxOrder = 0
        self.TaxRateRef = None


class TaxRateList(QuickbooksBaseObject):
    list_dict = {
        "TaxRateDetail": TaxRateDetail
    }

    qbo_object_name = "TaxRateList"

    def __init__(self):
        super(TaxRateList, self).__init__()
        self.TaxRateDetail = []


@python_2_unicode_compatible
class TaxCode(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The PaymentMethod entity provides the method of payment for received goods. Delete is achieved by setting the
    Active attribute to false in an entity update request; thus, making it inactive. In this type of delete,
    the record is not permanently deleted, but is hidden for display purposes. References to inactive objects are
    left intact.
    """

    class_dict = {
        "SalesTaxRateList": TaxRateList,
        "PurchaseTaxRateList": TaxRateList,
    }

    qbo_object_name = "TaxCode"

    def __init__(self):
        super(TaxCode, self).__init__()
        self.Name = ""
        self.Description = ""
        self.Taxable = True
        self.TaxGroup = True
        self.Active = True

        self.SalesTaxRateList = None
        self.PurchaseTaxRateList = None

    def __str__(self):
        return self.Name
