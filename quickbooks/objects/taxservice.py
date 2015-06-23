from base import QuickbooksBaseObject, Ref


'''
QBO definition: The TaxService endpoint allows you to perform the following actions:

 - Create a new tax code and specify a list of existing tax rates to be associated to that tax code. To retrieve a
   list of existing tax codes, query the TaxCode endpoint.
 - Create a new tax rate dynamically. To retrieve a list of existing tax rates, query the TaxRate endpoint.

Tax  agency entities on tax rates created via the TaxService endpoint are referenced by id only. That is, you
cannot create new tax agencies via the TaxService endpoint.
'''
class TaxService(QuickbooksBaseObject):
    class_dict = {
        "TaxRateDetails": TaxRateDetails
    }

    qbo_object_name = "TaxService"

    TaxCode = ""
    TaxCodeId = ""
    Active = True

    def __unicode__(self):
        return self.TaxCode


class TaxRateDetails(QuickbooksBaseObject):
    qbo_object_name = "TaxRateDetails"

    TaxRateName = ""
    TaxRateId = 0
    RateValue = 0
    TaxAgencyId = 0
    TaxApplicableOn = ""

    def __unicode__(self):
        return self.TaxRateName