from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Address, EmailAddress, Ref, CustomField, CustomerMemo, QuickbooksManagedObject, \
    LinkedTxnMixin, LinkedTxn, MarkupInfo, QuickbooksTransactionEntity
from .tax import TxnTaxDetail


@python_2_unicode_compatible
class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
        "MarkupInfo": MarkupInfo
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.Qty = 0
        self.UnitPrice = 0
        self.ServiceDate = ""
        self.TaxInclusiveAmt = 0

        self.MarkupInfo = None
        self.ItemRef = None
        self.TaxCodeRef = None
        self.ClassRef = None
        self.PriceLevelRef = None

    def __str__(self):
        return str(self.UnitPrice)


class SubtotalLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref
    }

    def __init__(self):
        super(SubtotalLineDetail, self).__init__()
        self.ItemRef = None


class DiscountOverride(QuickbooksBaseObject):
    class_dict = {
        "DiscountRef": Ref,
        "DiscountAccountRef": Ref
    }

    def __init__(self):
        super(DiscountOverride, self).__init__()
        self.PercentBased = False
        self.DiscountPercent = 0
        self.DiscountAccountRef = None
        self.DiscountRef = None


class DiscountLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
        "Discount": DiscountOverride
    }

    def __init__(self):
        super(DiscountLineDetail, self).__init__()
        self.ClassRef = None
        self.TaxCodeRef = None
        self.Discount = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(DescriptionLineDetail, self).__init__()
        self.ServiceDate = ""
        self.TaxCodeRef = None


@python_2_unicode_compatible
class CreditMemoLine(QuickbooksBaseObject):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail,
        "SubtotalLineDetail": SubtotalLineDetail,
        "DiscountLineDetail": DiscountLineDetail,
        "DescriptionLineDetail": DescriptionLineDetail
    }

    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField
    }

    def __init__(self):
        super(CreditMemoLine, self).__init__()
        self.Id = None
        self.LineNum = ""
        self.Description = ""
        self.Amount = ""
        self.DetailType = ""

        self.SubtotalLineDetail = None
        self.SalesItemLineDetail = None
        self.DiscountLineDetail = None
        self.DescriptionLineDetail = None

        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return "[{0}] {1} {2}".format(self.LineNum, self.Description, self.Amount)


@python_2_unicode_compatible
class CreditMemo(QuickbooksTransactionEntity, QuickbooksManagedObject, LinkedTxnMixin):
    """
    QBO definition: The CreditMemo is a financial transaction representing a refund or credit of payment or part
    of a payment for goods or services that have been sold.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "DepartmentRef": Ref,
        "ClassRef": Ref,
        "CustomerRef": Ref,
        "CurrencyRef": Ref,
        "SalesTermRef": Ref,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "TxnTaxDetail": TxnTaxDetail,
        "PaymentMethodRef": Ref,
        "DepositToAccountRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": CreditMemoLine
    }

    qbo_object_name = "CreditMemo"

    def __init__(self):
        super(CreditMemo, self).__init__()
        self.RemainingCredit = 0
        self.ExchangeRate = 0
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = ""
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0
        self.GlobalTaxCalculation = "TaxExcluded"

        self.BillAddr = None
        self.ShipAddr = None
        self.ClassRef = None
        self.DepartmentRef = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.BillEmail = None
        self.TxnTaxDetail = None
        self.SalesTermRef = None

        self.CustomField = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
