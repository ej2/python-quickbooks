from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, CustomField, Address, EmailAddress, CustomerMemo, QuickbooksManagedObject, \
    QuickbooksTransactionEntity, LinkedTxn, LinkedTxnMixin
from .tax import TxnTaxDetail
from .detailline import DetailLine
from ..mixins import QuickbooksPdfDownloadable


class DeliveryInfo(QuickbooksBaseObject):
    def __init__(self):
        super(DeliveryInfo, self).__init__()
        self.DeliveryType = ""
        self.DeliveryTime = ""


@python_2_unicode_compatible
class Invoice(QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: An Invoice represents a sales form where the customer pays for a product or service later.

    """

    class_dict = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "CustomerRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
        "DepositToAccountRef": Ref,
        "BillAddr": Address,
        "ShipAddr": Address,
        "TxnTaxDetail": TxnTaxDetail,
        "BillEmail": EmailAddress,
        "CustomerMemo": CustomerMemo,
        "DeliveryInfo": DeliveryInfo
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": DetailLine,
        "LinkedTxn": LinkedTxn,
    }

    qbo_object_name = "Invoice"

    def __init__(self):
        super(Invoice, self).__init__()
        self.Deposit = 0
        self.Balance = 0
        self.AllowIPNPayment = True
        self.DocNumber = ""
        self.PrivateNote = ""
        self.DueDate = ""
        self.ShipDate = ""
        self.TrackingNum = ""
        self.TotalAmt = ""
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"

        self.EInvoiceStatus = None

        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.DepartmentRef = None
        self.TxnTaxDetail = None
        self.DeliveryInfo = None

        self.CustomField = []
        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)

    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = "Invoice"
        linked_txn.TxnLineId = 1

        return linked_txn

    @property
    def email_sent(self):
        if self.EmailStatus == "EmailSent":
            return True

        return False
