from base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, \
    LinkedTxnMixin
from tax import TxnTaxDetail
from detailline import DetailLine


class JournalEntryLineDetail(QuickbooksBaseObject):
    class_dict = {
        "Entity": Ref
    }

    def __init__(self):
        super(JournalEntryLineDetail, self).__init__()
        self.PostingType = ""
        self.TaxApplicableOn = ""
        self.Type = ""
        self.TaxAmount = 0
        self.BillableStatus = ""

        self.Entity = None
        self.EntityRef = None
        self.AccountRef = None
        self.ClassRef = None
        self.DepartmentRef = None
        self.TaxCodeRef = None


class JournalEntryLine(DetailLine):
    class_dict = {
        "JournalEntryLineDetail": JournalEntryLineDetail
    }

    def __init__(self):
        super(JournalEntryLine, self).__init__()
        self.DetailType = "JournalEntryLineDetail"
        self.JournalEntryLineDetail = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(DescriptionLineDetail, self).__init__()
        self.ServiceDate = ""


class DescriptionOnlyLine(DetailLine):
    class_dict = {
        "DescriptionLineDetail": DescriptionLineDetail
    }

    def __init__(self):
        super(DescriptionOnlyLine, self).__init__()
        self.DetailType = "DescriptionOnly"


class JournalEntry(QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: Journal Entry is a transaction in which:
        - There are at least two parts - a Debit and a Credit - called distribution lines.
        - Each distribution line has an account from the Chart of Accounts.
        - The total of the Debit column equals the total of the Credit column.

        When you record a transaction with Journal Entry, the QBO UI labels the transaction as JRNL in a
        register and General Journal on reports that list transactions.
    """

    class_dict = {
        "TxnTaxDetail": TxnTaxDetail,
        "CurrencyRef": Ref,
    }

    list_dict = {
        "Line": JournalEntryLine
    }

    qbo_object_name = "JournalEntry"

    def __init__(self):
        super(JournalEntry, self).__init__()
        self.Adjustment = False
        self.TxnDate = ""
        self.TxnSource = ""
        self.DocNumber = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.Line = []
        self.TxnTaxDetail = None

        self.CurrencyRef = None

    def __unicode__(self):
        return str(self.TotalAmt)
