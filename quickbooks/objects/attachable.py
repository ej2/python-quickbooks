from .base import Ref, QuickbooksManagedObject, QuickbooksTransactionEntity, AttachableRef
from ..client import QuickBooks
from ..mixins import DeleteMixin


class Attachable(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: This page covers the Attachable, Upload, and Download resources used for attachment management. Attachments are supplemental information linked to a transaction or Item object. They can be files, notes, or a combination of both.
    In the case of file attachments, use an upload endpoint multipart request to upload the files to the QuickBooks attachment list and, optionally, to supply metadata for each via an attachable object. If meta data is not supplied with the upload request, the system creates it.
    In the case of a note, use the create attachable endpoint.
    For information about attachments, see the Attachments Developer Guide.
    """

    class_dict = {
        "EntityRef": Ref,
    }

    list_dict = {
        "AttachableRef": AttachableRef,
    }

    qbo_object_name = "Attachable"

    def __init__(self):
        super(Attachable, self).__init__()

        self.AttachableRef = []
        self.FileName = None
        self._FilePath = ''
        self.Note = ""
        self.FileAccessUri = None
        self.TempDownloadUri = None
        self.Size = None
        self.ContentType = None
        self.Category = None
        self.Lat = None
        self.Long = None
        self.PlaceName = None
        self.ThumbnailFileAccessUri = None
        self.ThumbnailTempDownloadUri = None

    def __str__(self):
        return self.FileName

    def to_ref(self):
        ref = Ref()
        ref.name = self.FileName
        ref.type = self.qbo_object_name
        ref.value = self.Id
        return ref

    def save(self, qb=None):
        if not qb:
            qb = QuickBooks()

        if self.Id and int(self.Id) > 0:
            json_data = qb.update_object(self.qbo_object_name, self.to_json(), _file_path=self._FilePath)
        else:
            json_data = qb.create_object(self.qbo_object_name, self.to_json(), _file_path=self._FilePath)

        if self.Id is None and self.FileName:
            obj = type(self).from_json(json_data['AttachableResponse'][0]['Attachable'])
        else:
            obj = type(self).from_json(json_data['Attachable'])

        self.Id = obj.Id

        return obj
