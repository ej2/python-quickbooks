from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, \
    LinkedTxnMixin, MarkupInfo
from .detailline import DetailLine


class ItemBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
        "TaxCodeRef": Ref,
        "MarkupInfo": MarkupInfo,
        "CustomerRef": Ref,
    }

    def __init__(self):
        super(ItemBasedExpenseLineDetail, self).__init__()
        self.BillableStatus = ""
        self.UnitPrice = 0
        self.Qty = 0
        self.TaxInclusiveAmt = 0


class ItemBasedExpenseLine(DetailLine):
    class_dict = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLineDetail,
    }

    def __init__(self):
        super(ItemBasedExpenseLine, self).__init__()

        self.DetailType = "ItemBasedExpenseLineDetail"
        self.ItemBasedExpenseLineDetail = None


class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref,
        "ClassRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref,
        "MarkupInfo": MarkupInfo,
    }

    def __init__(self):
        super(AccountBasedExpenseLineDetail, self).__init__()
        self.BillableStatus = ""
        self.TaxAmount = 0
        self.TaxInclusiveAmt = 0


class AccountBasedExpenseLine(DetailLine):
    class_dict = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail,
    }

    def __init__(self):
        super(AccountBasedExpenseLine, self).__init__()

        self.DetailType = "AccountBasedExpenseLineDetail"
        self.AccountBasedExpenseLineDetail = None


@python_2_unicode_compatible
class VendorCredit(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
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