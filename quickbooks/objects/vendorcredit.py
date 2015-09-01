from base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, LinkedTxnMixin


class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        super(AccountBasedExpenseLineDetail, self).__init__()
        self.BillableStatus = ""

    def __unicode__(self):
        return self.BillableStatus


class VendorCreditLine(QuickbooksBaseObject):
    class_dict = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail,
    }

    list_dict = {}

    def __init__(self):
        super(VendorCreditLine, self).__init__()
        self.Amount = 0
        self.DetailType = ""
        self.AccountBasedExpenseLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class VendorCredit(QuickbooksManagedObject, LinkedTxnMixin):
    """
    QBO definition: The Vendor Credit entity is an accounts payable transaction that represents a refund or credit
    of payment for goods or services. It is a credit that a vendor owes you for various reasons such as overpaid
    bill, returned merchandise, or other reasons.
    """
    class_dict = {
        "VendorRef": Ref,
        "APAccountRef": Ref,
    }

    list_dict = {
        "Line": VendorCreditLine
    }

    qbo_object_name = "VendorCredit"

    def __init__(self):
        super(VendorCredit, self).__init__()
        self.TotalAmt = 0
        self.FromAccountRef = None
        self.ToAccountRef = None

    def __unicode__(self):
        return str(self.TotalAmt)