from six import python_2_unicode_compatible
from .base import Ref, CustomField, QuickbooksManagedObject, LinkedTxnMixin, Address, \
    EmailAddress, QuickbooksTransactionEntity, LinkedTxn
from .tax import TxnTaxDetail
from .detailline import DetailLine
from ..mixins import QuickbooksPdfDownloadable, DeleteMixin


@python_2_unicode_compatible
class SalesReceipt(DeleteMixin, QuickbooksPdfDownloadable, QuickbooksManagedObject,
                   QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: SalesReceipt represents the sales receipt that is given to a customer.
    A sales receipt is similar to an invoice. However, for a sales receipt, payment is received
    as part of the sale of goods and services. The sales receipt specifies a deposit account
    where the customer deposits the payment. If the deposit account is not specified, the
    payment type is classified as Undeposited Account.
    """
    class_dict = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "DepositToAccountRef": Ref,
        "CustomerRef": Ref,
        "BillAddr": Address,
        "ShipAddr": Address,
        "ClassRef": Ref,
        "BillEmail": EmailAddress,
        "PaymentMethodRef": Ref,
        "ShipMethodRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": DetailLine,
        "LinkedTxn": LinkedTxn
    }

    detail_dict = {

    }

    qbo_object_name = "SalesReceipt"

    def __init__(self):
        super(SalesReceipt, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.ShipDate = ""
        self.TrackingNum = ""
        self.TotalAmt = 0
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0
        self.PaymentRefNum = ""
        self.ApplyTaxAfterDiscount = False
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"

        self.CustomerMemo = None
        self.DeliveryInfo = None
        self.CreditCardPayment = None
        self.TxnSource = None
        self.DepartmentRef = None
        self.CurrencyRef = None
        self.TxnTaxDetail = None
        self.DepositToAccountRef = None
        self.BillAddr = None
        self.ShipAddr = None
        self.ShipMethodRef = None
        self.BillEmail = None
        self.CustomerRef = None
        self.ClassRef = None
        self.PaymentMethodRef = None

        self.CustomField = []
        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)
