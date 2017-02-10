from six import python_2_unicode_compatible
from .base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin
from ..mixins import DeleteMixin


@python_2_unicode_compatible
class Transfer(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
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
        self.TxnDate = None
        self.PrivateNote = None
        self.TxnSource = None

        self.FromAccountRef = None
        self.ToAccountRef = None

    def __str__(self):
        return str(self.Amount)
