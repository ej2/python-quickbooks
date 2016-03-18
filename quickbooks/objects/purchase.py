from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, \
    LinkedTxn, Address, CustomField, MarkupInfo

from .tax import TxnTaxDetail


@python_2_unicode_compatible
class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ClassRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref
    }

    list_dict = {}

    def __init__(self):
        super(AccountBasedExpenseLineDetail, self).__init__()
        self.BillableStatus = ""
        self.ClassRef = None
        self.AccountRef = None
        self.TaxCodeRef = None

    def __str__(self):
        return self.BillableStatus


class ItemBasedExpenseLineDetail(QuickbooksBaseObject):

    class_dict = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
        "TaxCodeRef": Ref,
        "CustomerRef": Ref,
        "MarkupInfo": MarkupInfo
    }

    def __init__(self):

        self.UnitPrice = 0
        self.Qty = 0
        self.BillableStatus = ""
        self.TaxInclusiveAmt = 0

        self.ItemRef = None
        self.ClassRef = None
        self.PriceLevelRef = None
        self.TaxCodeRef = None
        self.CustomerRef = None
        self.MarkupInfo = None


@python_2_unicode_compatible
class PurchaseLine(QuickbooksBaseObject):
    class_dict = {
        "AccountBasedExpenseLineDetail": Ref,
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLineDetail,
    }

    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField,
    }

    def __init__(self):
        super(PurchaseLine, self).__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = "ItemBasedExpenseLineDetail"

        self.TaxCodeRef = None
        self.AccountRef = None
        self.ItemBasedExpenseLineDetail = None

        self.LinkedTxn = []
        self.AccountBasedExpenseLineDetail = []

    def __str__(self):
        return str(self.Amount)


@python_2_unicode_compatible
class Purchase(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: This entity represents expenses, such as a purchase made from a vendor.
    There are three types of Purchases: Cash, Check, and Credit Card.

     - Cash Purchase contains information regarding a payment made in cash.
     - Check Purchase contains information regarding a payment made by check.
     - Credit Card Purchase contains information regarding a payment made by credit card or refunded/credited back
       to a credit card.

    For example, to create a transaction that sends a check to a vendor, create a Purchase object with PaymentType
    set to Check. To query Purchase transactions of a certain type, for example Check, submit the following to the
    query endpoint: SELECT * from Purchase where PaymentType='Check' You must specify an AccountRef for all purchases.
    The TotalAmtattribute must add up to sum of Line.Amount attributes.
    """
    class_dict = {
        "AccountRef": Ref,
        "EntityRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "PaymentMethodRef": Ref,
        "RemitToAddr": Address,
        "TxnTaxDetail": TxnTaxDetail
    }

    list_dict = {
        "Line": PurchaseLine,
        "LinkedTxn": LinkedTxn,
    }

    qbo_object_name = "Purchase"

    def __init__(self):
        super(Purchase, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.ExchangeRate = 1
        self.PrivateNote = ""
        self.PaymentType = ""
        self.Credit = False
        self.TotalAmt = 0
        self.PrintStatus = "NeedToPrint"
        self.PurchaseEx = ""
        self.TxnSource = ""
        self.GlobalTaxCalculation = "TaxExcluded"

        self.TxnTaxDetail = None
        self.DepartmentRef = None
        self.AccountRef = None
        self.EnitityRef = None
        self.CurrencyRef = None
        self.PaymentMethodRef = None
        self.RemitToAddr = None

        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)
