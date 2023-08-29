from .base import Address, PhoneNumber, EmailAddress, WebAddress, MetaData, QuickbooksReadOnlyObject, \
    QuickbooksTransactionEntity


class CustomerType(QuickbooksReadOnlyObject, QuickbooksTransactionEntity):
    """
    QBO definition: Customer types allow categorizing customers in ways that are meaningful to the business.
    For example, one could set up customer types so that they indicate which industry a customer represents,
    a customer's geographic location, or how a customer first heard about the business. The categorization
    then can be used for reporting or mailings.
    """

    class_dict = {
        "MetaData": MetaData
    }

    qbo_object_name = "CustomerType"

    def __init__(self):
        super(CustomerType, self).__init__()
        self.Name = ""
        self.Active = False
        self.MetaData = None

    def __str__(self):
        return self.Name
