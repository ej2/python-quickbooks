from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, QuickbooksTransactionEntity, QuickbooksUpdateOnlyObject, Ref


class EmailMessageType(QuickbooksBaseObject):
    def __init__(self):
        super().__init__()
        self.Message = ""
        self.Subject = ""


class EmailMessagesPrefs(QuickbooksBaseObject):
    class_dict = {
        "InvoiceMessage": EmailMessageType,
        "EstimateMessage": EmailMessageType,
        "SalesReceiptMessage": EmailMessageType,
        "StatementMessage": EmailMessageType,
    }

    def __init__(self):
        super().__init__()
        self.InvoiceMessage = None
        self.EstimateMessage = None
        self.SalesReceiptMessage = None
        self.StatementMessage = None


class ProductAndServicesPrefs(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()
        self.QuantityWithPriceAndRate = True
        self.ForPurchase = True
        self.QuantityOnHand = True
        self.ForSales = True


class ReportPrefs(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()
        self.ReportBasis = "Accrual"  # or "Cash"
        self.CalcAgingReportFromTxnDate = False  # read only


class AccountingInfoPrefs(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()
        self.FirstMonthOfFiscalYear = "January"  # read only
        self.UseAccountNumbers = True  # read only
        self.TaxYearMonth = "January"  # read only
        self.ClassTrackingPerTxn = False
        self.TrackDepartments = False
        self.TaxForm = "6"
        # Possible values include: Clients, Customers, Donors, Guests, Members, Patients, Tenants.
        self.CustomerTerminology = ""  # Customers
        self.BookCloseDate = ""  # e.g. "2018-12-31"
        # Possible values include: Business, Department, Division, Location, Property, Store, Territory
        self.DepartmentTerminology = ""  # Location
        self.ClassTrackingPerTxnLine = True


class ClassTrackingPerTxnLine(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()
        self.ReportBasis = "Accrual"  # or "Cash"
        self.CalcAgingReportFromTxnDate = False  # read only


# class SalesFormsPrefs(QuickbooksBaseObject):  # FIXME
# class VendorAndPurchasesPrefs(QuickbooksBaseObject):  # FIXME
# class TaxPrefs(QuickbooksBaseObject):  # FIXME
# class OtherPrefs(QuickbooksBaseObject):  # FIXME
# class TimeTrackingPrefs(QuickbooksBaseObject):  # FIXME
# class CurrencyPrefs(QuickbooksBaseObject):  # FIXME


@python_2_unicode_compatible
class Preferences(QuickbooksUpdateOnlyObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Preferences resource represents a set of company preferences that
    control application behavior in QuickBooks Online.
    They are mostly exposed as read-only through the Preferences endpoint with only a very small subset of them
    available as writable. Preferences are not necessarily honored when making requests via the QuickBooks API
    because a lot of them control UI behavior in the application and may not be applicable for apps.
    """

    class_dict = {
        'EmailMessagesPrefs': EmailMessagesPrefs,
        'ProductAndServicesPrefs': ProductAndServicesPrefs,
        'ReportPrefs': ReportPrefs,
        'AccountingInfoPrefs': AccountingInfoPrefs,

        # FIXME: add remaining fields to be serializable, otherwise they will remain as dicts
        # 'SalesFormsPrefs': SalesFormsPrefs,
        # 'VendorAndPurchasesPrefs': VendorAndPurchasesPrefs,
        # 'TaxPrefs': TaxPrefs,
        # 'OtherPrefs': OtherPrefs,
        # 'TimeTrackingPrefs': TimeTrackingPrefs,
        # 'CurrencyPrefs': CurrencyPrefs,
    }

    qbo_object_name = "Preferences"

    def __init__(self):
        super().__init__()
        self.EmailMessagesPrefs = None
        self.ProductAndServicesPrefs = None
        self.ReportPrefs = None
        self.AccountingInfoPrefs = None
        self.SalesFormsPrefs = None
        self.VendorAndPurchasesPrefs = None
        self.TaxPrefs = None
        self.OtherPrefs = None
        self.TimeTrackingPrefs = None
        self.CurrencyPrefs = None

    def __str__(self):
        return 'Preferences {0}'.format(self.Id)
