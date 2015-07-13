from base import QuickbooksBaseObject, Ref


class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict = {
        "CustomerRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        self.BillableStatus = ""


class VendorCreditLine(QuickbooksBaseObject):
    class_dict = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail,
    }

    list_dict = {}

    def __init__(self):
        self.Amount = 0
        self.DetailType = ""
        self.AccountBasedExpenseLineDetail = None


class VendorCredit(QuickbooksBaseObject):
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
        self.TotalAmt = 0
        self.FromAccountRef = None
        self.ToAccountRef = None
