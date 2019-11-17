from six import python_2_unicode_compatible
from .base import QuickbooksBaseObject, ListMixin


@python_2_unicode_compatible
class Preferences(QuickbooksBaseObject, ListMixin):
    """
    NOTE: This is currently a read-only object.  It simply hasn't been fully implemented yet into the library.

    QBO definition:

        The Preferences resource represents a set of company preferences that control application behavior in
        QuickBooks Online. They are mostly exposed as read-only through the Preferences endpoint with only a very small subset
        of them available as writable. Preferences are not necessarily honored when making requests via the QuickBooks API
        because a lot of them control UI behavior in the application and may not be applicable for apps.
    """

    qbo_object_name = "Preferences"

    def __str__(self):
        return 'Preferences'
