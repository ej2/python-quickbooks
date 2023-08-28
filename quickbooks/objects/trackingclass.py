from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class Class(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Classes provide a way to track different segments of the business so they're
    not tied to a particular client or project. For example, you can define classes to break down
    the income and expenses for each business segment. Classes are applied to individual detail
    lines of a transaction. This is in contrast to Department objects, which are applied to the
    entire transaction.
    """

    class_dict = {
        "ParentRef": Ref
    }

    qbo_object_name = "Class"

    def __init__(self):
        super(Class, self).__init__()
        self.Name = ""
        self.SubClass = False
        self.FullyQualifiedName = ""
        self.Active = True

    def __str__(self):
        return self.Name

    def to_ref(self):
        ref = Ref()

        ref.name = self.Name
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
