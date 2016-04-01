from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, Address, QuickbooksManagedObject, LinkedTxnMixin, \
    QuickbooksTransactionEntity, CustomField, LinkedTxn, MarkupInfo
from .tax import TxnTaxDetail


class ItemBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
        "TaxCodeRef": Ref,
        "MarkupInfo": MarkupInfo
    }

    def __init__(self):
        super(ItemBasedExpenseLineDetail, self).__init__()
        self.UnitPrice = 0
        self.Qty = 0
        self.BillableStatus = ""
        self.TaxInclusiveAmt = 0

        self.PriceLevelRef = None
        self.CustomerRef = None
        self.ClassRef = None
        self.TaxCodeRef = None
        self.MarkupInfo = None


@python_2_unicode_compatible
class PurchaseOrderLine(QuickbooksBaseObject):
    class_dict = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLineDetail,
        "ItemRef": Ref,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
    }

    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField
    }

    def __init__(self):
        super(PurchaseOrderLine, self).__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = "ItemBasedExpenseLineDetail"
        self.BillableStatus = ""
        self.UnitPrice = 0
        self.Qty = 0

        self.ItemBasedExpenseLineDetail = None
        self.AccountBasedExpenseLineDetail = None
        self.ItemRef = None
        self.ClassRef = None
        self.TaxCodeRef = None

        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return str(self.Amount)


@python_2_unicode_compatible
class PurchaseOrder(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The PurchaseOrder entity is a non-posting transaction representing a request to purchase
    goods or services from a third party.
    """
    class_dict = {
        "VendorAddr": Address,
        "ShipAddr": Address,
        "VendorRef": Ref,
        "APAccountRef": Ref,
        "AttachableRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
        "TaxCodeRef": Ref,
        "CurrencyRef": Ref,
        "TxnTaxDetail": TxnTaxDetail
    }

    list_dict = {
        "Line": PurchaseOrderLine,
        "CustomField": CustomField,
        "LinkedTxn": LinkedTxn,
    }

    qbo_object_name = "PurchaseOrder"

    def __init__(self):
        super(PurchaseOrder, self).__init__()
        self.POStatus = ""
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.DueDate = ""
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"

        self.TxnTaxDetail = None
        self.VendorAddr = None
        self.ShipAddr = None
        self.VendorRef = None
        self.APAccountRef = None
        self.AttachableRef = None
        self.ClassRef = None
        self.SalesTermRef = None
        self.TaxCodeRef = None
        self.CurrencyRef = None
        self.TxnTaxDetail = None

        self.Line = []
        self.CustomField = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)
