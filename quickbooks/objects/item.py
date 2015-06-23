from base import QuickbooksBaseObject, Ref


'''
QBO definition: An item is a thing that your company buys, sells, or re-sells, such as products and services.
An item is shown as a line on an invoice or other sales form. The Item.Type attribute, which specifies how
the item is used, has one of the following values:

   Inventory - This type tracks merchandise that your business purchases, stocks, and re-sells as inventory.
   QuickBooks tracks the current number of inventory items in stock, cost of goods sold, and the asset value of
   the inventory after the purchase and sale of every item.

   Service - This type tracks services that you charge on the purchase and tracks merchandise you sell and buy that
   is not tracked as inventory. For example, specialized labor, consulting hours, and professional fees.
'''
class Item(QuickbooksBaseObject):
    class_dict = {
        "AssetAccountRef": Ref,
        "ExpenseAccountRef": Ref,
        "IncomeAccountRef": Ref
    }

    qbo_object_name = "Item"

    Name = ""
    Description = ""
    Active = True
    FullyQualifiedName = ""
    Taxable = ""
    UnitPrice = ""
    Type = ""
    PurchaseDesc = ""
    PurchaseCost = 0
    TrackQtyOnHand = True
    QtyOnHand = 0
    InvStartDate = ""

    AssetAccountRef = None
    ExpenseAccountRef = None
    IncomeAccountRef = None

    def __unicode__(self):
        return self.Name


