from .base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity


class Account(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Account is a component of a Chart Of Accounts, and is part of a Ledger. Used to record a total
    monetary amount allocated against a specific use. Accounts are one of five basic types: asset, liability,
    revenue (income), expenses, or equity. Delete is achieved by setting the Active attribute to false in an entity
    update request; thus, making it inactive. In this type of delete, the record is not permanently deleted, but
    is hidden for display purposes. References to inactive objects are left intact.
    """

    class_dict = {
        "CurrencyRef": Ref,
        "ParentRef": Ref,
        "TaxCodeRef": Ref,
    }

    qbo_object_name = "Account"

    def __init__(self):
        super(Account, self).__init__()

        self.Name = ""
        self.SubAccount = False
        self.FullyQualifiedName = ""
        self.Active = True
        self.Classification = None
        self.AccountType = None
        self.AccountSubType = ""
        self.Description = ""
        self.AcctNum = ""
        self.CurrentBalance = None  # Readonly
        self.CurrentBalanceWithSubAccounts = None  # Readonly
        self.CurrencyRef = None
        self.ParentRef = None
        self.TaxCodeRef = None

    def __str__(self):
        return self.FullyQualifiedName

    def to_ref(self):
        ref = Ref()
        ref.name = self.FullyQualifiedName
        ref.type = self.qbo_object_name
        ref.value = self.Id
        return ref
