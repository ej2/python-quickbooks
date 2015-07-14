from base import QuickbooksBaseObject, QuickbooksManagedObject


class TaxRateDetails(QuickbooksBaseObject):
    qbo_object_name = "TaxRateDetails"

    def __init__(self):
        super(TaxRateDetails, self).__init__()
        self.TaxRateName = ""
        self.TaxRateId = 0
        self.RateValue = 0
        self.TaxAgencyId = 0
        self.TaxApplicableOn = ""

    def __unicode__(self):
        return self.TaxRateName


class TaxService(QuickbooksManagedObject):
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

    qbo_object_name = "TaxService"

    def __init__(self):
        super(TaxService, self).__init__()
        self.TaxCode = ""
        self.TaxCodeId = ""
        self.Active = True

    def __unicode__(self):
        return self.TaxCode
