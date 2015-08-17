from base import QuickbooksBaseObject, Ref, QuickbooksManagedObject


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

    def __unicode__(self):
        return self.BillableStatus


class PurchaseLine(QuickbooksBaseObject):
    class_dict = {
        "AccountBasedExpenseLineDetail": Ref,
    }

    list_dict = {}

    def __init__(self):
        super(PurchaseLine, self).__init__()
        self.Amount = 0
        self.DetailType = ""

        self.TaxCodeRef = None
        self.AccountRef = None
        self.AccountBasedExpenseLineDetail = []

    def __unicode__(self):
        return str(self.Amount)


class Purchase(QuickbooksManagedObject):
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
    }

    list_dict = {
        "Line": PurchaseLine
    }

    qbo_object_name = "Purchase"

    def __init__(self):
        super(Purchase, self).__init__()
        self.PaymentType = ""
        self.Credit = False
        self.TotalAmt = 0
        self.TxnDate = ""

    def __unicode__(self):
        return str(self.TotalAmt)
