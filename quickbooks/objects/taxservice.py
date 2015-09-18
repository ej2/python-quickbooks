from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject
from ..mixins import UpdateMixin


@python_2_unicode_compatible
class TaxRateDetails(QuickbooksBaseObject):
    qbo_object_name = "TaxRateDetails"

    def __init__(self):
        super(TaxRateDetails, self).__init__()
        self.TaxRateName = ""
        self.TaxRateId = False
        self.RateValue = ""
        self.TaxAgencyId = ""
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

    Tax  agency entities on tax rates created via the TaxService endpoint are referenced by id only. That is, you
    cannot create new tax agencies via the TaxService endpoint.
    """

    class_dict = {
        "TaxRateDetails": TaxRateDetails
    }

    qbo_object_name = "TaxService/Taxcode"

    def __init__(self):
        super(TaxService, self).__init__()
        self.TaxCode = ""
        self.TaxCodeId = ""

        self.TaxRateDetails = None

    def __str__(self):
        return self.TaxCode
