from base import QuickbooksBaseObject, Ref, LinkedTxn


class DepositLine(QuickbooksBaseObject):
    class_dict = {
        "DepositToAccountRef": Ref
    }

    list_dict = {
        "LinkedTxn": LinkedTxn
    }

    qbo_object_name = "Deposit"

    def __init__(self):
        self.Amount = 0
        self.LinkedTxn = []


class Deposit(QuickbooksBaseObject):
    """
    QBO definition: A deposit object is a transaction that records one or more deposits of the following types:

        -A customer payment, originally held in the Undeposited Funds account, into the Asset Account specified by
        the Deposit.DepositToAccountRef attribute. The Deposit.line.LinkedTxn sub-entity is used in this
        case to hold deposit information.

        -A new direct deposit specified by Deposit.Line.DepositLineDetail line detail.
    """

    class_dict = {
        "DepositToAccountRef": Ref
    }

    list_dict = {
        "Line": DepositLine
    }

    qbo_object_name = "Deposit"

    def __init__(self):
        self.TotalAmt = 0
        self.TxnDate = ""
        self.DepositToAccountRef = None
        self.Line = []
