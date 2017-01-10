from six import python_2_unicode_compatible

from quickbooks.objects.detailline import SalesItemLine, SubtotalLine, DiscountLine, DescriptionLine, DetailLine
from .base import Address, EmailAddress, Ref, CustomField, CustomerMemo, QuickbooksManagedObject, \
    LinkedTxnMixin, QuickbooksTransactionEntity
from .tax import TxnTaxDetail


@python_2_unicode_compatible
class CreditMemo(QuickbooksTransactionEntity, QuickbooksManagedObject, LinkedTxnMixin):
    """
    QBO definition: The CreditMemo is a financial transaction representing a refund or credit of payment or part
    of a payment for goods or services that have been sold.
    """

    class_dict = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "DepartmentRef": Ref,
        "ClassRef": Ref,
        "CustomerRef": Ref,
        "CurrencyRef": Ref,
        "SalesTermRef": Ref,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "TxnTaxDetail": TxnTaxDetail,
        "PaymentMethodRef": Ref,
        "DepositToAccountRef": Ref,
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": DetailLine
    }

    detail_dict = {
        "SalesItemLineDetail": SalesItemLine,
        "SubTotalLineDetail": SubtotalLine,
        "DiscountLineDetail": DiscountLine,
        "DescriptionLineDetail": DescriptionLine
    }

    qbo_object_name = "CreditMemo"

    def __init__(self):
        super(CreditMemo, self).__init__()
        self.RemainingCredit = 0
        self.ExchangeRate = 0
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = ""
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0
        self.GlobalTaxCalculation = "TaxExcluded"

        self.BillAddr = None
        self.ShipAddr = None
        self.ClassRef = None
        self.DepartmentRef = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.BillEmail = None
        self.TxnTaxDetail = None
        self.SalesTermRef = None

        self.CustomField = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
