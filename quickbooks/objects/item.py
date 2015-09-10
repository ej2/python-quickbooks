from base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity


class Item(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: An item is a thing that your company buys, sells, or re-sells, such as products and services.
    An item is shown as a line on an invoice or other sales form. The Item.Type attribute, which specifies how
    the item is used, has one of the following values:

       Inventory - This type tracks merchandise that your business purchases, stocks, and re-sells as inventory.
       QuickBooks tracks the current number of inventory items in stock, cost of goods sold, and the asset value of
       the inventory after the purchase and sale of every item.

       Service - This type tracks services that you charge on the purchase and tracks merchandise you sell and buy that
       is not tracked as inventory. For example, specialized labor, consulting hours, and professional fees.
    """

    class_dict = {
        "AssetAccountRef": Ref,
        "ExpenseAccountRef": Ref,
        "IncomeAccountRef": Ref,
        "ParentRef": Ref,
        "SalesTaxCodeRef": Ref,
        "PurchaseTaxCodeRef": Ref,
    }

    qbo_object_name = "Item"

    def __init__(self):
        super(Item, self).__init__()
        self.Name = ""
        self.Description = ""
        self.Active = True
        self.SubItem = False
        self.FullyQualifiedName = ""
        self.Taxable = False
        self.SalesTaxInclusive = False
        self.UnitPrice = ""
        self.Type = "Inventory"
        self.ItemCategoryType = "Product"
        self.Level = 0
        self.PurchaseDesc = ""
        self.PurchaseTaxInclusive = False
        self.PurchaseCost = 0
        self.TrackQtyOnHand = False
        self.QtyOnHand = 0
        self.InvStartDate = ""

        self.AbatementRate = ""
        self.ReverseChargeRate = ""
        self.ServiceType = ""

        self.AssetAccountRef = None
        self.ExpenseAccountRef = None
        self.IncomeAccountRef = None
        self.SalesTaxCodeRef = None
        self.ParentRef = None
        self.PurchaseTaxCodeRef = None

    def __unicode__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()

        ref.name = self.Name
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref

