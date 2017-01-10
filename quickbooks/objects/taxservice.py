from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject
from ..mixins import UpdateMixin
from ..client import QuickBooks


@python_2_unicode_compatible
class TaxRateDetails(QuickbooksBaseObject):
    qbo_object_name = "TaxRateDetails"

    def __init__(self):
        super(TaxRateDetails, self).__init__()
        self.TaxRateName = None
        self.TaxRateId = None
        self.RateValue = None
        self.TaxAgencyId = None
        self.TaxApplicableOn = "Sales"

    def __str__(self):
        return self.TaxRateName


@python_2_unicode_compatible
class TaxService(QuickbooksBaseObject, UpdateMixin):
    """
    QBO definition: The TaxService endpoint allows you to perform the following actions:

     - Create a new tax code and specify a list of existing tax rates to be associated to that tax code. To retrieve a
       list of existing tax codes, query the TaxCode endpoint.
     - Create a new tax rate dynamically. To retrieve a list of existing tax rates, query the TaxRate endpoint.

    Tax agency entities on tax rates created via the TaxService endpoint are referenced by id only. That is, you
    cannot create new tax agencies via the TaxService endpoint.
    """

    list_dict = {
        "TaxRateDetails": TaxRateDetails
    }

    qbo_object_name = "TaxService/Taxcode"

    def __init__(self):
        super(TaxService, self).__init__()
        self.TaxCode = None  # Required
        self.TaxCodeId = None  # Readonly - this is the unique database Id (called Id on every other model...)

        self.Id = 0
        self.TaxRateDetails = []

    def __str__(self):
        return self.TaxCode

    def save(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if self.TaxCodeId and self.TaxCodeId > 0:
            json_data = qb.update_object(self.qbo_object_name, self.to_json())
        else:
            json_data = qb.create_object(self.qbo_object_name, self.to_json())

        obj = type(self).from_json(json_data)
        self.TaxCodeId = obj.Id
        self.Id = self.TaxCodeId

        return obj
