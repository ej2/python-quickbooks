from base import Ref, QuickbooksManagedObject, LinkedTxnMixin


class Transfer(QuickbooksManagedObject, LinkedTxnMixin):
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
        super(Transfer, self).__init__()
        self.Amount = 0
        self.FromAccountRef = None
        self.ToAccountRef = None

    def __unicode__(self):
        return str(self.Amount)
