from base import QuickbooksBaseObject, Ref, Address, QuickbooksManagedObject
from purchase import AccountBasedExpenseLineDetail


class ItemBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref
    }

    def __init__(self):
        super(ItemBasedExpenseLineDetail, self).__init__()
        self.CustomerRef = None


class PurchaseOrderLine(QuickbooksBaseObject):
    class_dict = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLineDetail,
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail,
        "ItemRef": Ref,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        super(PurchaseOrderLine, self).__init__()
        self.Description = ""
        self.Amount = 0
        self.DetailType = ""
        self.BillableStatus = ""
        self.UnitPrice = 0
        self.Qty = 0

        self.ItemBasedExpenseLineDetail = None
        self.AccountBasedExpenseLineDetail = None
        self.ItemRef = None
        self.ClassRef = None
        self.TaxCodeRef = None

    def __unicode__(self):
        return str(self.Amount)


class PurchaseOrder(QuickbooksManagedObject):
    """
    QBO definition: The PurchaseOrder entity is a non-posting transaction representing a request to purchase
    goods or services from a third party.
    """
    class_dict = {
        "VendorAddr": Address,
        "ShipAddr": Address,
        "VendorRef": Ref,
        "APAccountRef": Ref
    }

    list_dict = {
        "Line": PurchaseOrderLine,
    }

    qbo_object_name = "PurchaseOrder"

    def __init__(self):
        super(PurchaseOrder, self).__init__()
        self.POStatus = ""
        self.DocNumber = ""
        self.TxnDate = ""
        self.TotalAmt = 0
        self.VendorAddr = None
        self.ShipAddr = None
        self.VendorRef = None
        self.APAccountRef = None
        self.Line = []

    def __unicode__(self):
        return str(self.TotalAmt)
