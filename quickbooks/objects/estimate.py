from six import python_2_unicode_compatible
from .base import CustomField, Ref, CustomerMemo, Address, EmailAddress, QuickbooksManagedObject, \
    LinkedTxnMixin, QuickbooksTransactionEntity, LinkedTxn
from .tax import TxnTaxDetail
from .detailline import DetailLine, SalesItemLine, GroupLine, DescriptionLine, DiscountLine, SubtotalLine
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

    detail_dict = {
        "SalesItemLineDetail": SalesItemLine,
        "GroupLineDetail": GroupLine,
        "DescriptionOnly": DescriptionLine,
        "DiscountLineDetail": DiscountLine,
        "SubTotalLineDetail": SubtotalLine,
    }

    qbo_object_name = "Estimate"

    def __init__(self):
        super(Estimate, self).__init__()
        self.DocNumber = None
        self.TxnDate = None
        self.TxnStatus = None
        self.PrivateNote = None
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.DueDate = None
        self.ShipDate = None
        self.ExpirationDate = None
        self.AcceptedBy = None
        self.AcceptedDate = None
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
