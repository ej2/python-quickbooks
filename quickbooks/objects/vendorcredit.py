from six import python_2_unicode_compatible

from .base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, \
    LinkedTxnMixin
from .detailline import DetailLine, AccountBasedExpenseLine, ItemBasedExpenseLine, TDSLine
from ..mixins import DeleteMixin


@python_2_unicode_compatible
class VendorCredit(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The Vendor Credit entity is an accounts payable transaction that represents a refund or credit
    of payment for goods or services. It is a credit that a vendor owes you for various reasons such as overpaid
    bill, returned merchandise, or other reasons.
    """
    class_dict = {
        "VendorRef": Ref,
        "APAccountRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
    }

    list_dict = {
        "Line": DetailLine
    }

    detail_dict = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "VendorCredit"

    def __init__(self):
        super(VendorCredit, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"

        self.FromAccountRef = None
        self.ToAccountRef = None

        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)