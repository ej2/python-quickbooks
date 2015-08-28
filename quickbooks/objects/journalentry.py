from base import QuickbooksBaseObject, Ref, QuickbooksManagedObject, QuickbooksTransactionEntity
from tax import TxnTaxDetail


class Entity(QuickbooksBaseObject):
    class_dict = {
        "EntityRef": Ref
    }

    def __init__(self):
        super(Entity, self).__init__()
        self.Type = ""
        self.EntityRef = None


class JournalEntryLineDetail(QuickbooksBaseObject):
    class_dict = {
        "AccountRef": Ref,
        "Entity": Ref
    }

    def __init__(self):
        super(JournalEntryLineDetail, self).__init__()
        self.PostingType = ""
        self.Entity = None
        self.AccountRef = None

    def __unicode__(self):
        return self.PostingType


class JournalEntryLine(QuickbooksBaseObject):
    class_dict = {
        "JournalEntryLineDetail": JournalEntryLineDetail
    }

    def __init__(self):
        super(JournalEntryLine, self).__init__()
        self.Description = ""
        self.Amount = 0
        self.Id = 0
        self.LineNum = 0
        self.DetailType = "JournalEntryLineDetail"
        self.JournalEntryLineDetail = None

    def __unicode__(self):
        return str(self.Amount)


class JournalEntry(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Journal Entry is a transaction in which:
        - There are at least two parts - a Debit and a Credit - called distribution lines.
        - Each distribution line has an account from the Chart of Accounts.
        - The total of the Debit column equals the total of the Credit column.

        When you record a transaction with Journal Entry, the QBO UI labels the transaction as JRNL in a
        register and General Journal on reports that list transactions.
    """

    class_dict = {
        "TxnTaxDetail": TxnTaxDetail
    }

    list_dict = {
        "Line": JournalEntryLine
    }

    qbo_object_name = "JournalEntry"

    def __init__(self):
        super(JournalEntry, self).__init__()
        self.Adjustment = False
        self.TxnDate = ""
        self.TotalAmt = 0
        self.Line = []
        self.TxnTaxDetail = None

    def __unicode__(self):
        return str(self.TotalAmt)
