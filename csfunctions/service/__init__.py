from csfunctions.metadata import MetaData
from csfunctions.service.file_upload import FileUploadService
from csfunctions.service.numgen import NumberGeneratorService


class Service:
    """
    Provides access to services on the elements instance, e.g. generating numbers.
    """

    def __init__(self, metadata: MetaData):
        self.generator = NumberGeneratorService(metadata=metadata)
        self.file_upload = FileUploadService(metadata=metadata)
