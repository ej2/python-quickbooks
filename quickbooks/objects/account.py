from base import QuickbooksBaseObject, Ref

'''
QBO definition: Account is a component of a Chart Of Accounts, and is part of a Ledger. Used to record a total
monetary amount allocated against a specific use. Accounts are one of five basic types: asset, liability,
revenue (income), expenses, or equity. Delete is achieved by setting the Active attribute to false in an entity
update request; thus, making it inactive. In this type of delete, the record is not permanently deleted, but
is hidden for display purposes. References to inactive objects are left intact.
'''
class Account(QuickbooksBaseObject):
    class_dict = {
        "CurrencyRef": Ref,
    }

    qbo_object_name = "Account"

    Name = ""
    SubAccount = False
    FullyQualifiedName = ""
    Active = True
    Classification = ""
    AccountType = ""
    AccountSubType = ""
    CurrentBalance = 0
    CurrentBalanceWithSubAccounts = 0
    CurrencyRef = None

    def __unicode__(self):
        return self.FullyQualifiedName
