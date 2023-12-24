from quickbooks.mixins import ListMixin, UpdateNoIdMixin, FromJsonMixin
from .base import CustomField, QuickbooksBaseObject


class ExchangeRateMetaData(FromJsonMixin):
    def __init__(self):
        self.LastUpdatedTime = ""


class ExchangeRate(QuickbooksBaseObject, ListMixin, UpdateNoIdMixin):
    """
    QBO definition: Applicable only for those companies that enable multicurrency,
    the exchangerate resource provides the ability to query and set exchange rates available to the
    QuickBooks Online company. This entity works in combination with the companycurrency entity
    and the Currency Center in the QuickBooks Online UI to manage exchange rates for the company.
    """

    class_dict = {
        "MetaData": ExchangeRateMetaData,
        "CustomField": CustomField,
    }

    qbo_object_name = "ExchangeRate"

    def __str__(self):
        return self.SourceCurrencyCode

    def __init__(self):
        super(ExchangeRate, self).__init__()

        self.AsOfDate = ""
        self.SourceCurrencyCode = ""
        self.Rate = 0
        self.TargetCurrencyCode = ""
        self.MetaData = None
        self.CustomField = None
