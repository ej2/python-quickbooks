from .base import QuickbooksBaseObject, Ref, CustomField, Address, EmailAddress, CustomerMemo, QuickbooksManagedObject, \
    QuickbooksTransactionEntity, LinkedTxn, LinkedTxnMixin, MetaData
from .tax import TxnTaxDetail
from .detailline import DetailLine, SalesItemLine, SubtotalLine, DiscountLine, GroupLine, DescriptionOnlyLine
from ..mixins import QuickbooksPdfDownloadable, DeleteMixin, SendMixin, VoidMixin


class DeliveryInfo(QuickbooksBaseObject):
    def __init__(self):
        super(DeliveryInfo, self).__init__()
        self.DeliveryType = ""
        self.DeliveryTime = ""


class Invoice(DeleteMixin, QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity,
              LinkedTxnMixin, SendMixin, VoidMixin):
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
        "BillEmailCc": EmailAddress,
        "BillEmailBcc": EmailAddress,
        "CustomerMemo": CustomerMemo,
        "DeliveryInfo": DeliveryInfo,
        "RecurDataRef": Ref,
        "TaxExemptionRef": Ref,
        "MetaData": MetaData
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": DetailLine,
        "LinkedTxn": LinkedTxn,
    }

    detail_dict = {
        "SalesItemLineDetail": SalesItemLine,
        "SubTotalLineDetail": SubtotalLine,
        "DiscountLineDetail": DiscountLine,
        "DescriptionOnly": DescriptionOnlyLine,
        "GroupLineDetail": GroupLine
    }

    qbo_object_name = "Invoice"

    def __init__(self):
        super(Invoice, self).__init__()
        self.Deposit = 0
        self.Balance = 0
        self.AllowIPNPayment = True
        self.AllowOnlineCreditCardPayment = False
        self.AllowOnlineACHPayment = False
        self.DocNumber = None

        self.PrivateNote = ""
        self.DueDate = ""
        self.ShipDate = ""
        self.TrackingNum = ""
        self.TotalAmt = ""
        self.TxnDate = ""
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"
        self.InvoiceLink = ""
        self.HomeBalance = 0
        self.HomeTotalAmt = 0
        self.FreeFormAddress = False

        self.EInvoiceStatus = None

        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.BillEmailCc = None
        self.BillEmailBcc = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.DepartmentRef = None
        self.TxnTaxDetail = None
        self.DeliveryInfo = None
        self.RecurDataRef = None
        self.SalesTermRef = None
        self.ShipMethodRef = None
        self.TaxExemptionRef = None
        self.MetaData = None

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

    def to_ref(self):
        ref = Ref()

        ref.name = self.DocNumber
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
