from base import QuickbooksBaseObject, Ref, CustomField, QuickbooksManagedObject
from tax import TxnTaxDetail


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.ItemRef = None
        self.TaxCodeRef = None


class RefundReceiptLine(QuickbooksBaseObject):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(RefundReceiptLine, self).__init__()
        self.LineNum = ""
        self.Amount = 0
        self.DetailType = ""

        self.SalesItemLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class RefundReceipt(QuickbooksManagedObject):
    """
    QBO definition: RefundReceipt represents a refund to the customer for a product or service that was given.
    """
    class_dict = {
        "DepartmentRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "DepositToAccountRef": Ref
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": RefundReceiptLine,
    }

    qbo_object_name = "RefundReceipt"

    def __init__(self):
        super(RefundReceipt, self).__init__()
        self.DocNumber = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = ""
        self.Balance = 0
        self.PaymentRefNum = ""

        self.DepartmentRef = None
        self.TxnTaxDetail = None
        self.DepositToAccountRef = None
        self.CustomField = []
        self.Line = []

    def __unicode__(self):
        return str(self.TotalAmt)
