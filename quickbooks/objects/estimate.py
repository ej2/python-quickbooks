from base import QuickbooksBaseObject, CustomField, Ref, CustomerMemo, Address, EmailAddress, QuickbooksManagedObject, \
    LinkedTxnMixin, QuickbooksTransactionEntity, LinkedTxn
from tax import TxnTaxDetail


class EstimateLine(QuickbooksBaseObject):
    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField,
    }

    def __init__(self):
        super(EstimateLine, self).__init__()
        self.Id = 0
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = ""
        self.LinkedTxn = []
        self.CustomField = []

    def __unicode__(self):
        return str(self.Amount)


class DiscountOverride(QuickbooksBaseObject):
    class_dict = {
        "DiscountRef": Ref,
        "DiscountAccountRef": Ref,
    }

    qbo_object_name = "DiscountOverride"

    def __init__(self):
        super(DiscountOverride, self).__init__()
        self.PercentBased = False
        self.DiscountPercent = 0
        self.DiscountRef = None
        self.DiscountAccountRef = None


class DiscountLineDetail(QuickbooksBaseObject):
    class_dict = {
        "Discount": DiscountOverride,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        super(DiscountLineDetail, self).__init__()

        self.Discount = None
        self.ClassRef = None
        self.TaxCodeRef = None


class DiscountLine(EstimateLine):
    class_dict = {
        "DiscountLineDetail": DiscountLineDetail
    }

    def __init__(self):
        super(DiscountLine, self).__init__()
        self.DetailType = "DiscountLineDetail"
        self.DiscountLineDetail = None


class SubtotalLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref
    }

    def __init__(self):
        super(SubtotalLineDetail, self).__init__()
        self.ItemRef = None


class SubtotalLine(EstimateLine):
    class_dict = {
        "SubtotalLineDetail": SubtotalLineDetail
    }

    def __init__(self):
        super(SubtotalLine, self).__init__()
        self.DetailType = "SubtotalLineDetail"
        self.SubtotalLineDetail = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(DescriptionLineDetail, self).__init__()
        self.ServiceDate = ""
        self.TaxCodeRef = None


class DescriptionLine(EstimateLine):
    class_dict = {
        "DescriptionLineDetail": DescriptionLineDetail
    }

    def __init__(self):
        super(DescriptionLine, self).__init__()
        self.DetailType = "DescriptionOnly"
        self.DescriptionLineDetail = None


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
        "PriceLevelRef": Ref,
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.UnitPrice = 0
        self.Qty = 0
        self.MarkupInfo = ""
        self.ServiceDate = ""
        self.TaxInclusiveAmt = 0

    def __unicode__(self):
        return str(self.UnitPrice)


class SaleItemLine(EstimateLine):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(SaleItemLine, self).__init__()
        self.DetailType = "SalesItemLineDetail"
        self.SalesItemLineDetail = None


class Estimate(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The Estimate represents a proposal for a financial transaction from a business to a customer
    for goods or services proposed to be sold, including proposed pricing.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "CustomerRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "LinkedTxn": LinkedTxn,
        "Line": EstimateLine,
    }

    qbo_object_name = "Estimate"

    def __init__(self):
        super(Estimate, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.TxnStatus = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.DueDate = ""
        self.ShipDate = ""
        self.ExpirationDate = ""
        self.AcceptedBy = ""
        self.AcceptedDate = ""
        self.GlobalTaxCalculation = "TaxExcluded"
        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerRef = None
        self.TxnTaxDetail = None
        self.CustomerMemo = None
        self.ClassRef = None
        self.SalesTermRef = None
        self.ShipMethodRef = None

        self.CustomField = []
        self.LinkedTxn = []
        self.Line = []

    def __unicode__(self):
        return str(self.TotalAmt)
