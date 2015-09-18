from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, Ref, CustomField, LinkedTxn, MarkupInfo


@python_2_unicode_compatible
class DetailLine(QuickbooksBaseObject):
    list_dict = {
        "LinkedTxn": LinkedTxn,
        "CustomField": CustomField,
    }

    def __init__(self):
        super(DetailLine, self).__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = ""
        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return "[{0}] {1} {2}".format(self.LineNum, self.Description, self.Amount)


class DiscountOverride(QuickbooksBaseObject):
    class_dict = {
        "DiscountRef": Ref,
        "DiscountAccountRef": Ref,
    }

    qbo_object_name = "DiscountOverride"

    def __init__(self):
        super(DiscountOverride, self).__init__()
        self.PercentBased = False
        self.DiscountPercent = 0
        self.DiscountRef = None
        self.DiscountAccountRef = None


class DiscountLineDetail(QuickbooksBaseObject):
    class_dict = {
        "Discount": DiscountOverride,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        super(DiscountLineDetail, self).__init__()

        self.Discount = None
        self.ClassRef = None
        self.TaxCodeRef = None


class DiscountLine(DetailLine):
    class_dict = {
        "DiscountLineDetail": DiscountLineDetail
    }

    def __init__(self):
        super(DiscountLine, self).__init__()
        self.DetailType = "DiscountLineDetail"
        self.DiscountLineDetail = None


class SubtotalLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref
    }

    def __init__(self):
        super(SubtotalLineDetail, self).__init__()
        self.ItemRef = None


class SubtotalLine(DetailLine):
    class_dict = {
        "SubtotalLineDetail": SubtotalLineDetail
    }

    def __init__(self):
        super(SubtotalLine, self).__init__()
        self.DetailType = "SubtotalLineDetail"
        self.SubtotalLineDetail = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict = {
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(DescriptionLineDetail, self).__init__()
        self.ServiceDate = ""
        self.TaxCodeRef = None


class DescriptionLine(DetailLine):
    class_dict = {
        "DescriptionLineDetail": DescriptionLineDetail
    }

    def __init__(self):
        super(DescriptionLine, self).__init__()
        self.DetailType = "DescriptionOnly"
        self.DescriptionLineDetail = None


@python_2_unicode_compatible
class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
        "PriceLevelRef": Ref,
        "MarkupInfo": MarkupInfo,
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.UnitPrice = 0
        self.Qty = 0
        self.ServiceDate = ""
        self.TaxInclusiveAmt = 0

        self.MarkupInfo = None
        self.ItemRef = None
        self.ClassRef = None
        self.TaxCodeRef = None
        self.PriceLevelRef = None

    def __str__(self):
        return str(self.UnitPrice)


class SaleItemLine(DetailLine):
    class_dict = {
        "SalesItemLineDetail": SalesItemLineDetail
    }

    def __init__(self):
        super(SaleItemLine, self).__init__()
        self.DetailType = "SalesItemLineDetail"
        self.SalesItemLineDetail = None
