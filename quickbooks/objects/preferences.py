from quickbooks.mixins import PrefMixin, UpdateNoIdMixin
from .base import QuickbooksBaseObject, QuickbooksTransactionEntity, Ref, EmailAddress


class PreferencesCustomField(QuickbooksBaseObject):
    def __init__(self):
        self.Type = ""
        self.Name = ""
        self.StringValue = ""
        self.BooleanValue = ""

    def __str__(self):
        return self.Name


class PreferencesCustomFieldGroup(QuickbooksBaseObject):
    list_dict = {
        "CustomField": PreferencesCustomField
    }

    def __init__(self):
        super().__init__()


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
        self.RevenueRecognition = True
        self.RevenueRecognitionFrequency = ""


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
        "DefaultTerms": Ref,
        "SalesEmailBcc": EmailAddress,
        "SalesEmailCc": EmailAddress
    }
    detail_dict = {
        "CustomField": PreferencesCustomFieldGroup
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
        self.DefaultShippingAccount = False
        self.AllowDeposit = True
        self.AutoApplyPayments = True
        self.IPNSupportEnabled = False
        self.AutoApplyCredit = True
        self.CustomField = None
        self.UsingPriceLevels = False
        self.ETransactionAttachPDF = False
        self.UsingProgressInvoicing = False
        self.EstimateMessage = ""

        self.DefaultTerms = None
        self.CustomField = None
        self.SalesEmailBcc = None
        self.SalesEmailCc = None


class VendorAndPurchasesPrefs(QuickbooksBaseObject):
    class_dict = {
        "DefaultTerms": Ref,
        "DefaultMarkupAccount": Ref
    }
    detail_dict = {
        "POCustomField": PreferencesCustomFieldGroup
    }

    def __init__(self):
        super().__init__()
        self.BillableExpenseTracking = True
        self.TrackingByCustomer = True
        self.TPAREnabled = True

        self.POCustomField = None
        self.DefaultMarkupAccount = None
        self.DefaultTerms = None


class TaxPrefs(QuickbooksBaseObject):
    class_dict = {
        "TaxGroupCodeRef": Ref
    }

    def __init__(self):
        super().__init__()
        self.TaxGroupCodeRef = None
        self.UsingSalesTax = True
        self.PartnerTaxEnabled = True


class NameValue(QuickbooksBaseObject):
    def __init__(self):
        super().__init__()
        self.Name = ""
        self.Value = ""


class OtherPrefs(QuickbooksBaseObject):
    list_dict = {
        "NameValue": NameValue
    }

    def __init__(self):
        super().__init__()
        self.NameValue = None


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
        "HomeCurrency": Ref
    }

    def __init__(self):
        super().__init__()
        self.HomeCurrency = None
        self.MultiCurrencyEnabled = False


class Preferences(PrefMixin, UpdateNoIdMixin, QuickbooksTransactionEntity):
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
