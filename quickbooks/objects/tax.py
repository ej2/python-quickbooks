from base import QuickbooksBaseObject, Address, EmailAddress, Ref, CustomField, CustomerMemo


class TaxLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxRateRef": Ref
    }

    def __init__(self):
        self.PercentBased = True
        self.TaxPercent = 0
        self.NetAmountTaxable = 0


class TaxLine(QuickbooksBaseObject):
    class_dict = {
        "TaxLineDetail": TaxLineDetail
    }

    def __init__(self):
        self.Amount = 0
        self.DetailType = ""


class TxnTaxDetail(QuickbooksBaseObject):
    class_dict = {
        "TxnTaxCodeRef": Ref,
    }

    list_dict = {
        "TaxLine": TaxLine
    }

    def __init__(self):
        self.TotalTax = 0
        self.TxnTaxCodeRef = None
        self.TaxLine = []