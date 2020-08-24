from six import python_2_unicode_compatible

from quickbooks.objects import CreditCardPayment
from .base import Ref, CustomField, QuickbooksManagedObject, \
    LinkedTxnMixin, QuickbooksTransactionEntity, LinkedTxn, Address, EmailAddress, QuickbooksBaseObject, CustomerMemo
from .tax import TxnTaxDetail
from .detailline import DetailLine
from ..mixins import DeleteMixin


@python_2_unicode_compatible
class RefundReceiptCheckPayment(QuickbooksBaseObject):
    qbo_object_name = "CheckPayment"

    def __init__(self):
        super(RefundReceiptCheckPayment, self).__init__()
        self.CheckNum = ""
        self.Status = ""
        self.NameOnAcct = ""
        self.AcctNum = ""
        self.BankName = ""

    def __str__(self):
        return self.CheckNum


@python_2_unicode_compatible
class RefundReceipt(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: RefundReceipt represents a refund to the customer for a product or service that was given.
    """
    class_dict = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "DepositToAccountRef": Ref,
        "CustomerRef": Ref,
        "BillAddr":  Address,
        "ShipAddr":  Address,
        "ClassRef": Ref,
        "BillEmail": EmailAddress,
        "PaymentMethodRef": Ref,
        "CheckPayment": RefundReceiptCheckPayment,
        "CreditCardPayment": CreditCardPayment,
        "CustomerMemo": CustomerMemo,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": DetailLine,
        "LinkedTxn": LinkedTxn
    }

    detail_dict = {

    }

    qbo_object_name = "RefundReceipt"

    def __init__(self):
        super(RefundReceipt, self).__init__()
        self.DocNumber = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.Balance = 0
        self.PaymentRefNum = ""
        self.TxnDate = ""
        self.ExchangeRate = 1
        self.PrivateNote = ""

        self.PaymentRefNum = ""
        self.PaymentType = ""

        self.TxnSource = None
        self.GlobalTaxCalculation = "TaxExcluded"

        self.DepartmentRef = None
        self.CurrencyRef = None
        self.TxnTaxDetail = None
        self.DepositToAccountRef = None
        self.CustomerRef = None
        self.BillAddr = None
        self.ShipAddr = None
        self.ClassRef = None
        self.BillEmail = None
        self.PaymentMethodRef = None
        self.CheckPayment = None
        self.CreditCardPayment = None
        self.CustomerMemo = None

        self.CustomField = []
        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)
