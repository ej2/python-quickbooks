from base import QuickbooksBaseObject, Address, EmailAddress, Ref, CustomField, CustomerMemo, QuickbooksManagedObject
from tax import TxnTaxDetail


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.Qty = 0
        self.UnitPrice = 0

        self.ItemRef = None
        self.TaxCodeRef = None

    def __unicode__(self):
        return str(self.UnitPrice)


class CreditMemoLine(QuickbooksBaseObject):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(CreditMemoLine, self).__init__()
        self.LineNum = ""
        self.Description = ""
        self.Amount = ""
        self.DetailType = ""

        self.SalesItemLineDetail = None

    def __unicode__(self):
        return "[{0}] {1} {2}".format(self.LineNum, self.Description, self.Amount)


class CreditMemo(QuickbooksManagedObject):
    """
    QBO definition: The CreditMemo is a financial transaction representing a refund or credit of payment or part
    of a payment for goods or services that have been sold.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "DepartmentRef": Ref,
        "CustomerRef": Ref,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "TxnTaxDetail": TxnTaxDetail,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": CreditMemoLine
    }

    qbo_object_name = "CreditMemo"

    def __init__(self):
        super(CreditMemo, self).__init__()
        self.RemainingCredit = ""
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = ""
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0

        self.BillAddr = None
        self.ShipAddr = None
        self.DepartmentRef = None
        self.CustomerRef = None
        self.CustomerMemo = None
        self.BillEmail = None

        self.CustomField = []
        self.Line = []

    def __unicode__(self):
        return str(self.TotalAmt)
