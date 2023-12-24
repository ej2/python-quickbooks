from .base import QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class Department(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: The Department entity provides a way to track different segments of the business, divisions, or
    physical locations such as stores, and allows another way of categorizing the entire transaction.
    This is in contrast to Class objects, which are applied to individual transaction line details.
    Delete is achieved by setting the Active attribute to false in an entity update request; thus,
    making it inactive. In this type of delete, the record is not permanently deleted, but is hidden
    for display purposes. References to inactive objects are left intact.
    """

    class_dict = {
        "ParentRef": Ref
    }

    qbo_object_name = "Department"

    def __init__(self):
        super(Department, self).__init__()
        self.Name = ""
        self.SubDepartment = False
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
