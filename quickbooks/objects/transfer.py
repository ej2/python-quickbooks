from base import QuickbooksBaseObject, Ref


class Transfer(QuickbooksBaseObject):
    """
    QBO definition: A Transfer represents a transaction where funds are moved between two accounts from the
    company's QuickBooks chart of accounts.
    """
    class_dict = {
        "FromAccountRef": Ref,
        "ToAccountRef": Ref,
    }

    qbo_object_name = "Transfer"

    def __init__(self):
        self.Amount = 0
        self.FromAccountRef = None
        self.ToAccountRef = None
