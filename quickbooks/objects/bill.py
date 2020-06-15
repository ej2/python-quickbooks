from six import python_2_unicode_compatible

from quickbooks.objects.detailline import DetailLine, ItemBasedExpenseLine, AccountBasedExpenseLine, \
    TDSLine
from .base import Ref, LinkedTxn, QuickbooksManagedObject, QuickbooksTransactionEntity, \
    LinkedTxnMixin
from .tax import TxnTaxDetail
from ..mixins import DeleteMixin


@python_2_unicode_compatible
class Bill(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A Bill entity is an AP transaction representing a request-for-payment from a third party for
    goods/services rendered and/or received.
    """

    class_dict = {
        "SalesTermRef": Ref,
        "CurrencyRef": Ref,
        "APAccountRef": Ref,
        "VendorRef": Ref,
        "AttachableRef": Ref,
        "DepartmentRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
    }

    list_dict = {
        "Line": DetailLine,
        "LinkedTxn": LinkedTxn,
    }

    detail_dict = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "Bill"

    def __init__(self):
        super(Bill, self).__init__()

        self.DueDate = ""
        self.Balance = 0
        self.TotalAmt = ""
        self.TxnDate = ""
        self.DocNumber = ""
        self.PrivateNote = ""
        self.ExchangeRate = 0
        self.GlobalTaxCalculation = None

        self.SalesTermRef = None
        self.CurrencyRef = None
        self.AttachableRef = None
        self.VendorRef = None
        self.DepartmentRef = None
        self.APAccountRef = None

        self.LinkedTxn = []
        self.Line = []

    def __str__(self):
        return str(self.Balance)

    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = "Bill"
        linked_txn.TxnLineId = 1

        return linked_txn

    def to_ref(self):
        ref = Ref()

        ref.name = self.DocNumber
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref

