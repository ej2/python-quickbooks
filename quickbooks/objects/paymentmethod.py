from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class PaymentMethod(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The PaymentMethod entity provides the method of payment for received goods. Delete is achieved by setting the
    Active attribute to false in an entity update request; thus, making it inactive. In this type of delete,
    the record is not permanently deleted, but is hidden for display purposes. References to inactive objects are
    left intact.
    """

    class_dict = {}

    qbo_object_name = "PaymentMethod"

    def __init__(self):
        super(PaymentMethod, self).__init__()
        self.Name = ""
        self.Type = ""
        self.Active = True

    def __str__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()
        ref.name = self.Name
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
