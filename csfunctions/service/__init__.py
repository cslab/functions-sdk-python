from csfunctions.metadata import MetaData
from csfunctions.service.base import Conflict, NotFound, Unauthorized, UnprocessableEntity
from csfunctions.service.file_upload import FileUploadService
from csfunctions.service.numgen import NumberGeneratorService
from csfunctions.service.temp_file import TempFileService

__all__ = [
    "Service",
    "FileUploadService",
    "NumberGeneratorService",
    "TempFileService",
    "Conflict",
    "NotFound",
    "Unauthorized",
    "UnprocessableEntity",
]


class Service:
    """
    Provides access to services on the elements instance, e.g. generating numbers.
    """

    def __init__(self, metadata: MetaData):
        self.generator = NumberGeneratorService(metadata=metadata)
        self.file_upload = FileUploadService(metadata=metadata)
        self.temp_file = TempFileService(metadata=metadata)
