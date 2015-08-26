from base import QuickbooksBaseObject, CustomField, Ref, CustomerMemo, Address, EmailAddress, QuickbooksManagedObject
from tax import TxnTaxDetail

class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.UnitPrice = 0
        self.Qty = 0

    def __unicode__(self):
        return str(self.UnitPrice)


class EstimateLine(QuickbooksBaseObject):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(EstimateLine, self).__init__()
        self.LineNum = 0
        self.Amount = 0
        self.Description = ""
        self.DetailType = ""
        self.SalesItemLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class Estimate(QuickbooksManagedObject):
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
    }

    list_dict = {
        "CustomField": CustomField,
    }

    qbo_object_name = "Estimate"

    def __init__(self):
        super(Estimate, self).__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.TxnStatus = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = 0
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.BillAddr = None
        self.ShipAddr = None
        self.CustomerRef = None
        self.TxnTaxDetail = None
        self.CustomerMemo = None
        self.CustomField = []

    def __unicode__(self):
        return str(self.TotalAmt)
