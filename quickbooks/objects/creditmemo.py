from base import QuickbooksBaseObject, Address, EmailAddress, Ref, CustomField, CustomerMemo, QuickbooksManagedObject, \
    LinkedTxnMixin, LinkedTxn
from tax import TxnTaxDetail


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.Qty = 0
        self.UnitPrice = 0
        self.MarkupInfo = ""
        self.ServiceDate = ""
        self.TaxInclusiveAmt = 0

        self.ItemRef = None
        self.TaxCodeRef = None
        self.ClassRef = None
        self.PriceLevelRef = None

    def __unicode__(self):
        return str(self.UnitPrice)


class SubtotalLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref
    }

    def __init__(self):
        self.ItemRef = None


class DiscountOverride(QuickbooksBaseObject):
    class_dict = {
        "DiscountRef": Ref,
        "DiscountAccountRef": Ref
    }

    def __init__(self):
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
        self.ClassRef = None
        self.TaxCodeRef = None
        self.Discount = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxCodeRef": Ref
    }

    def __init__(self):
        self.ServiceDate = ""
        self.TaxCodeRef = None


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
        self.Id = ""
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

    def __unicode__(self):
        return "[{0}] {1} {2}".format(self.LineNum, self.Description, self.Amount)


class CreditMemo(QuickbooksManagedObject, LinkedTxnMixin):
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
        self.CustomerMemo = ""
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

    def __unicode__(self):
        return str(self.TotalAmt)
