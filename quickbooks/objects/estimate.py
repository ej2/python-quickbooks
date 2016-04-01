from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, CustomField, Ref, CustomerMemo, Address, EmailAddress, QuickbooksManagedObject, \
    LinkedTxnMixin, QuickbooksTransactionEntity, LinkedTxn
from .tax import TxnTaxDetail
from .detailline import DetailLine
from ..mixins import QuickbooksPdfDownloadable


@python_2_unicode_compatible
class Estimate(QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The Estimate represents a proposal for a financial transaction from a business to a customer
    for goods or services proposed to be sold, including proposed pricing.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "CustomerRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "LinkedTxn": LinkedTxn,
        "Line": DetailLine,
    }

    qbo_object_name = "Estimate"

    def __init__(self):
        super(Estimate, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.TxnStatus = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.DueDate = ""
        self.ShipDate = ""
        self.ExpirationDate = ""
        self.AcceptedBy = ""
        self.AcceptedDate = ""
        self.GlobalTaxCalculation = "TaxExcluded"
        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerRef = None
        self.TxnTaxDetail = None
        self.CustomerMemo = None
        self.ClassRef = None
        self.SalesTermRef = None
        self.ShipMethodRef = None

        self.CustomField = []
        self.LinkedTxn = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
