from quickbooks.mixins import ListMixin, ReadMixin
from .base import QuickbooksTransactionEntity, Ref, QuickbooksBaseObject


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


class TaxCode(QuickbooksTransactionEntity, QuickbooksBaseObject, ReadMixin, ListMixin):
    """
    QBO definition: A TaxCode object is used to track the taxable or non-taxable status of products,
    services, and customers. You can assign a sales tax code to each of your products, services,
    and customers based on their taxable or non-taxable status. You can then use these codes to generate
    reports that provide information to the tax agencies about the taxable or non-taxable status of
    certain sales. See Global tax model for more information about using TaxCode objects and the tax model in general.
    """

    class_dict = {
        "SalesTaxRateList": TaxRateList,
        "PurchaseTaxRateList": TaxRateList,
    }

    qbo_object_name = "TaxCode"

    def __init__(self):
        super(TaxCode, self).__init__()
        # All values are readonly - TaxCodes are created with the taxservice api
        self.Name = None
        self.Description = None
        self.Taxable = None
        self.TaxGroup = None
        self.Active = True

        self.SalesTaxRateList = None
        self.PurchaseTaxRateList = None

    def __str__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()

        ref.type = self.qbo_object_name
        ref.value = self.Id
        ref.name = self.Name

        return ref
