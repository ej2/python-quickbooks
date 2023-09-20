from .base import QuickbooksBaseObject, Ref, LinkedTxn, QuickbooksManagedObject, LinkedTxnMixin, \
    QuickbooksTransactionEntity
from ..mixins import DeleteMixin, VoidMixin


class CheckPayment(QuickbooksBaseObject):
    class_dict = {
        "BankAccountRef": Ref
    }

    qbo_object_name = "CheckPayment"

    def __init__(self):
        super(CheckPayment, self).__init__()
        self.PrintStatus = "NotSet"
        self.BankAccountRef = None

    def __str__(self):
        return self.PrintStatus


class BillPaymentCreditCard(QuickbooksBaseObject):
    class_dict = {
        "CCAccountRef": Ref
    }

    qbo_object_name = "BillPaymentCreditCard"

    def __init__(self):
        super(BillPaymentCreditCard, self).__init__()
        self.CCAccountRef = None


class BillPaymentLine(QuickbooksBaseObject):
    list_dict = {
        "LinkedTxn": LinkedTxn
    }

    qbo_object_name = "Line"

    def __init__(self):
        super(BillPaymentLine, self).__init__()
        self.Amount = 0
        self.LinkedTxn = []

    def __str__(self):
        return str(self.Amount)


class BillPayment(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, VoidMixin):
    """
    QBO definition: A BillPayment entity represents the financial transaction of payment
    of bills that the business owner receives from a vendor for goods or services purchased
    from the vendor. QuickBooks Online supports bill payments through a credit card or a
    checking account. BillPayment.TotalAmt is the total amount associated with this payment.
    This includes the total of all the payments from the payment line details. If TotalAmt is
    greater than the total on the lines being paid, the overpayment is treated as a credit and
    exposed as such on the QuickBooks UI. The total amount cannot be negative.
    """

    class_dict = {
        "VendorRef": Ref,
        "CheckPayment": CheckPayment,
        "CreditCardPayment": BillPaymentCreditCard,
        "APAccountRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref
    }

    list_dict = {
        "Line": BillPaymentLine
    }

    qbo_object_name = "BillPayment"

    def __init__(self):
        super(BillPayment, self).__init__()
        self.PayType = ""
        self.TotalAmt = 0
        self.PrivateNote = ""
        self.DocNumber = ""

        self.VendorRef = None
        self.CheckPayment = None
        self.APAccountRef = None
        self.DepartmentRef = None
        self.CreditCardPayment = None
        self.CurrencyRef = None

        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
