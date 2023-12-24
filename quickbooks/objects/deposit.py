from .base import QuickbooksBaseObject, Ref, LinkedTxn, QuickbooksManagedObject, LinkedTxnMixin, \
    QuickbooksTransactionEntity, CustomField, AttachableRef
from ..mixins import DeleteMixin


class CashBackInfo(QuickbooksBaseObject):
    class_dict = {
        "AccountRef": Ref
    }

    def __init__(self):
        super(CashBackInfo, self).__init__()
        self.Amount = 0
        self.Memo = ""
        self.AccountRef = None


class DepositLineDetail(QuickbooksBaseObject):
    class_dict = {
        "Entity": Ref,
        "ClassRef": Ref,
        "AccountRef": Ref,
        "PaymentMethodRef": Ref,
    }

    def __init__(self):
        super(DepositLineDetail, self).__init__()
        self.CheckNum = ""
        self.TxnType = None

        self.Entity = None
        self.ClassRef = None
        self.AccountRef = None
        self.PaymentMethodRef = None


class DepositLine(QuickbooksBaseObject):
    class_dict = {
        "DepositToAccountRef": Ref,
        "DepositLineDetail": DepositLineDetail,
    }

    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField,
    }

    qbo_object_name = "Deposit"

    def __init__(self):
        super(DepositLine, self).__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = "DepositLineDetail"
        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return str(self.Amount)


class Deposit(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A deposit object is a transaction that records one or more deposits of the following types:

        -A customer payment, originally held in the Undeposited Funds account, into the Asset Account specified by
        the Deposit.DepositToAccountRef attribute. The Deposit.line.LinkedTxn sub-entity is used in this
        case to hold deposit information.

        -A new direct deposit specified by Deposit.Line.DepositLineDetail line detail.
    """

    class_dict = {
        "DepositToAccountRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "AttachableRef": AttachableRef,
        "CashBack": CashBackInfo,
    }

    list_dict = {
        "Line": DepositLine
    }

    detail_dict = {
        "DepositLineDetail": DepositLine
    }

    qbo_object_name = "Deposit"

    def __init__(self):
        super(Deposit, self).__init__()
        self.TotalAmt = 0
        self.HomeTotalAmt = 0
        self.TxnDate = ""
        self.DocNumber = ""
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"
        self.PrivateNote = ""
        self.TxnStatus = ""
        self.TxnSource = None

        self.DepositToAccountRef = None
        self.DepartmentRef = None
        self.CurrencyRef = None
        self.AttachableRef = None
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
