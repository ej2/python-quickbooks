from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, QuickbooksTransactionEntity, QuickbooksUpdateOnlyObject  # CustomField, Ref


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


class SalesFormsPrefs(QuickbooksBaseObject):
    class_dict = {
        # 'DefaultTerms': Ref,  # FIXME: serialize field properly, not as JSON
    }
    list_dict = {
        # 'CustomField': CustomField,  # FIXME: serialize field properly, not as JSON
    }
    detail_dict = {
        # 'CustomField': CustomField,  # FIXME: serialize field properly, not as JSON
    }

    def __init__(self):
        super().__init__()
        self.ETransactionPaymentEnabled = False
        self.CustomTxnNumbers = False
        self.AllowShipping = False
        self.AllowServiceDate = False
        self.ETransactionEnabledStatus = ""  # e.g. "NotApplicable"
        self.DefaultCustomerMessage = ""  # e.g. "Thank you for your business and have a great day!"
        self.EmailCopyToCompany = False
        self.AllowEstimates = True
        self.DefaultTerms = None
        self.AllowDiscount = True
        self.DefaultDiscountAccount = ""
        self.AllowDeposit = True
        self.AutoApplyPayments = True
        self.IPNSupportEnabled = False
        self.AutoApplyCredit = True
        self.CustomField = None
        self.UsingPriceLevels = False
        self.ETransactionAttachPDF = False


class VendorAndPurchasesPrefs(QuickbooksBaseObject):
    class_dict = {}
    list_dict = {
        # 'POCustomField': CustomField,  # FIXME: serialize field properly, not as JSON
    }
    detail_dict = {
        # 'POCustomField': CustomField,  # FIXME: serialize field properly, not as JSON
    }

    def __init__(self):
        super().__init__()
        self.BillableExpenseTracking = True
        self.TrackingByCustomer = True
        self.POCustomField = None


class TaxPrefs(QuickbooksBaseObject):
    class_dict = {
        # 'TaxGroupCodeRef': Ref,  # FIXME: serialize field properly, not as JSON
    }

    def __init__(self):
        super().__init__()
        self.TaxGroupCodeRef = None
        self.UsingSalesTax = True


class OtherPrefs(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()


class TimeTrackingPrefs(QuickbooksBaseObject):

    def __init__(self):
        super().__init__()
        self.WorkWeekStartDate = ""  # e.g. "Monday"
        self.MarkTimeEntriesBillable = True
        self.ShowBillRateToAll = False
        self.UseServices = True
        self.BillCustomers = True


class CurrencyPrefs(QuickbooksBaseObject):
    class_dict = {
        # 'HomeCurrency': Ref,  # FIXME: serialize field properly, not as JSON
    }

    def __init__(self):
        super().__init__()
        self.HomeCurrency = None


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
        'SalesFormsPrefs': SalesFormsPrefs,
        'VendorAndPurchasesPrefs': VendorAndPurchasesPrefs,
        'TaxPrefs': TaxPrefs,
        'OtherPrefs': OtherPrefs,
        'TimeTrackingPrefs': TimeTrackingPrefs,
        'CurrencyPrefs': CurrencyPrefs,
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
