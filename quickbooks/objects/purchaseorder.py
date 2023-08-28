from quickbooks.objects.detailline import DetailLine, ItemBasedExpenseLine, AccountBasedExpenseLine, \
    TDSLine
from .base import Ref, Address, QuickbooksManagedObject, LinkedTxnMixin, \
    QuickbooksTransactionEntity, CustomField, LinkedTxn
from .tax import TxnTaxDetail
from ..mixins import DeleteMixin, SendMixin


class PurchaseOrder(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, SendMixin):
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
        "Line": DetailLine,
        "CustomField": CustomField,
        "LinkedTxn": LinkedTxn,
    }

    detail_dict = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "PurchaseOrder"

    def __init__(self):
        super(PurchaseOrder, self).__init__()
        self.POStatus = None
        self.DocNumber = None
        self.TxnDate = None
        self.PrivateNote = None
        self.TotalAmt = 0
        self.DueDate = None
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"
        self.Memo = None
        self.ShipMethodRef = None

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
