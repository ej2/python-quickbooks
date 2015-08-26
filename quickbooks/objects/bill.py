from base import QuickbooksBaseObject, Ref, LinkedTxn, QuickbooksManagedObject, QuickbooksTransactionEntity


class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref
    }

    def __init__(self):
        self.BillableStatus = ""

        self.CustomerRef = None
        self.AccountRef = None
        self.TaxCodeRef = None

    def __unicode__(self):
        return self.BillableStatus


class BillLine(QuickbooksBaseObject):
    class_dict = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail
    }

    def __init__(self):
        super(BillLine, self).__init__()

        self.LineNum = 0
        self.Description = ""
        self.Amount = ""
        self.DetailType = "AccountBasedExpenseLineDetail"

        self.AccountBasedExpenseLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class Bill(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: A Bill entity is an AP transaction representing a request-for-payment from a third party for
    goods/services rendered and/or received.
    """

    class_dict = {
        "SalesTermRef": Ref,
        "CurrencyRef": Ref,
        "APAccountRef": Ref,
        "VendorRef": Ref,
    }

    list_dict = {
        "Line": BillLine,
        "LinkedTxn": LinkedTxn
    }

    qbo_object_name = "Bill"

    def __init__(self):
        super(Bill, self).__init__()

        self.DueDate = ""
        self.Balance = 0
        self.TotalAmt = ""
        self.TxnDate = ""

        self.SalesTermRef = None
        self.CurrencyRef = None

        self.VendorRef = None
        self.APAccountRef = None

        self.LinkedTxn = []
        self.Line = []

    def __unicode__(self):
        return str(self.Balance)


