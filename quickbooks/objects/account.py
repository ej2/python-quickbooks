from base import QuickbooksBaseObject, Ref


class Account(QuickbooksBaseObject):
    """
    QBO definition: Account is a component of a Chart Of Accounts, and is part of a Ledger. Used to record a total
    monetary amount allocated against a specific use. Accounts are one of five basic types: asset, liability,
    revenue (income), expenses, or equity. Delete is achieved by setting the Active attribute to false in an entity
    update request; thus, making it inactive. In this type of delete, the record is not permanently deleted, but
    is hidden for display purposes. References to inactive objects are left intact.
    """

    class_dict = {
        "CurrencyRef": Ref,
    }

    qbo_object_name = "Account"

    def __init__(self):
        self.Name = ""
        self.SubAccount = False
        self.FullyQualifiedName = ""
        self.Active = True
        self.Classification = ""
        self.AccountType = ""
        self.AccountSubType = ""
        self.CurrentBalance = 0
        self.CurrentBalanceWithSubAccounts = 0
        self.CurrencyRef = None

    def __unicode__(self):
        return self.FullyQualifiedName
