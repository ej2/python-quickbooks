from base import QuickbooksBaseObject, Ref, CustomField, QuickbooksManagedObject
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
        self.ItemRef = None
        self.TaxCodeRef = None

    def __unicode__(self):
        return str(self.UnitPrice)


class SalesReceiptLine(QuickbooksBaseObject):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(SalesReceiptLine, self).__init__()
        self.LineNum = ""
        self.Description = ""
        self.Amount = 0
        self.DetailType = ""

        self.SalesItemLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class SalesReceipt(QuickbooksManagedObject):
    """
    QBO definition: SalesReceipt represents the sales receipt that is given to a customer. A sales receipt is
    similar to an invoice. However, for a sales receipt, payment is received as part of the sale of goods and
    services. The sales receipt specifies a deposit account where the customer deposits the payment. If the
    deposit account is not specified, the payment type is classified as Undeposited Account.
    """
    class_dict = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "DepositToAccountRef": Ref,
        "CustomerRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": SalesReceiptLine,
    }

    qbo_object_name = "SalesReceipt"

    def __init__(self):
        super(SalesReceipt, self).__init__()
        self.DocNumber = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0
        self.PaymentRefNum = ""
        self.ApplyTaxAfterDiscount = False

        self.DepositToAccountRef = None
        self.CurrencyRef = None
        self.DepartmentRef = None
        self.CustomerRef = None
        self.TxnTaxDetail = None
        self.CustomField = []
        self.Line = []

    def __unicode__(self):
        return str(self.TotalAmt)
