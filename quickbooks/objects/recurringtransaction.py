from .bill import Bill
from .creditmemo import CreditMemo
from .deposit import Deposit
from .estimate import Estimate
from .invoice import Invoice
from .journalentry import JournalEntry
from .purchase import Purchase
from .purchaseorder import PurchaseOrder
from .refundreceipt import RefundReceipt
from .salesreceipt import SalesReceipt
from .transfer import Transfer
from .vendorcredit import VendorCredit
from .base import Ref, QuickbooksBaseObject
from ..mixins import UpdateNoIdMixin, ListMixin, ReadMixin, DeleteNoIdMixin


class ScheduleInfo(QuickbooksBaseObject):
    def __init__(self):
        super(ScheduleInfo, self).__init__()

        self.StartDate = None
        self.EndDate = None
        self.DaysBefore = None
        self.MaxOccurrences = None

        self.RemindDays = None
        self.IntervalType = None
        self.NumInterval = None

        self.DayOfMonth = None
        self.DayOfWeek = None
        self.MonthOfYear = None
        self.WeekOfMonth = None

        self.NextDate = None
        self.PreviousDate = None


class RecurringInfo(QuickbooksBaseObject):
    class_dict = {
        "ScheduleInfo": ScheduleInfo
    }

    qbo_object_name = "RecurringInfo"

    def __init__(self):
        super(RecurringInfo, self).__init__()

        self.RecurType = "Automated"
        self.Name = ""
        self.Active = False


class Recurring():
    class_dict = {
        "RecurringInfo": RecurringInfo,
        "RecurDataRef": Ref
    }


class RecurringBill(Bill):
    class_dict = {**Bill.class_dict, **Recurring.class_dict}


class RecurringPurchase(Purchase):
    class_dict = {**Purchase.class_dict, **Recurring.class_dict}


class RecurringCreditMemo(CreditMemo):
    class_dict = {**CreditMemo.class_dict, **Recurring.class_dict}


class RecurringDeposit(Deposit):
    class_dict = {**Deposit.class_dict, **Recurring.class_dict}


class RecurringEstimate(Estimate):
    class_dict = {**Estimate.class_dict, **Recurring.class_dict}


class RecurringInvoice(Invoice):
    class_dict = {**Invoice.class_dict, **Recurring.class_dict}


class RecurringJournalEntry(JournalEntry):
    class_dict = {**JournalEntry.class_dict, **Recurring.class_dict}


class RecurringRefundReceipt(RefundReceipt):
    class_dict = {**RefundReceipt.class_dict, **Recurring.class_dict}


class RecurringSalesReceipt(SalesReceipt):
    class_dict = {**SalesReceipt.class_dict, **Recurring.class_dict}


class RecurringTransfer(Transfer):
    class_dict = {**Transfer.class_dict, **Recurring.class_dict}


class RecurringVendorCredit(VendorCredit):
    class_dict = {**VendorCredit.class_dict, **Recurring.class_dict}


class RecurringPurchaseOrder(PurchaseOrder):
    class_dict = {**PurchaseOrder.class_dict, **Recurring.class_dict}


class RecurringTransaction(QuickbooksBaseObject, ReadMixin, UpdateNoIdMixin, ListMixin, DeleteNoIdMixin):
    """
    QBO definition: A RecurringTransaction object refers to scheduling creation of transactions,
    set up reminders and create transaction template for later use.
    This feature is available in QuickBooks Essentials and Plus SKU.
    """
    class_dict = {
        "Bill": RecurringBill,
        "Purchase": RecurringPurchase,
        "CreditMemo": RecurringCreditMemo,
        "Deposit": RecurringDeposit,
        "Estimate": RecurringEstimate,
        "Invoice": RecurringInvoice,
        "JournalEntry": RecurringJournalEntry,
        "RefundReceipt": RecurringRefundReceipt,
        "SalesReceipt": RecurringSalesReceipt,
        "Transfer": RecurringTransfer,
        "VendorCredit": RecurringVendorCredit,
        "PurchaseOrder": RecurringPurchaseOrder
    }

    qbo_object_name = "RecurringTransaction"
