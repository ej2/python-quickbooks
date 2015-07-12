from base import QuickbooksBaseObject, Ref
from tax import TxnTaxDetail


class JournalEntryLineDetail(QuickbooksBaseObject):
    class_dict = {
        "AccountRef": Ref
    }

    def __init__(self):
        self.PostingType = ""
        self.AccountRef = None


class JournalEntryLine(QuickbooksBaseObject):
    class_dict = {
        "JournalEntryLineDetail": JournalEntryLineDetail
    }

    def __init__(self):
        self.Description = ""
        self.Amount = 0
        self.DetailType = ""


class JournalEntry(QuickbooksBaseObject):
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
        self.Adjustment = False
        self.TxnDate = ""
