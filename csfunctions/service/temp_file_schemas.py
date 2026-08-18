from pydantic import BaseModel, Field

from csfunctions.service.file_upload_schemas import PresignedWriteUrls

DEFAULT_MIMETYPE = "application/octet-stream"


class CreateTempFileRequest(BaseModel):
    """
    Request model for creating a temporary file.
    """

    filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The name the file will have when the user downloads it.",
    )
    mimetype: str = Field(
        DEFAULT_MIMETYPE,
        max_length=255,
        description="The MIME type of the file content.",
    )
    filesize: int = Field(..., description="The size of the file you want to upload in bytes.", ge=0)
    persno: str = Field(..., description="The persno of the user who will be allowed to download the file.")


class CreateTempFileResponse(BaseModel):
    """
    Response model for creating a temporary file.
    """

    temp_file_id: str = Field(..., description="The ID of the newly created temporary file.")
    presigned_write_urls: PresignedWriteUrls = Field(..., description="The presigned write URLs for the upload.")


class CompleteTempFileUploadRequest(BaseModel):
    """
    Request model for completing the upload of a temporary file.

    There is no filesize or sha256 here, because temporary files have no
    attributes to store them in.
    """

    presigned_write_urls: PresignedWriteUrls = Field(
        ..., description="The presigned write URLs for the upload, including the etags of the uploaded parts."
    )
    persno: str = Field(..., description="The persno of the user who is uploading the file.")


class AbortTempFileUploadRequest(BaseModel):
    """
    Request model for aborting the upload of a temporary file.
    """

    presigned_write_urls: PresignedWriteUrls = Field(..., description="The presigned write URLs for the upload.")
    persno: str = Field(..., description="The persno of the user who is uploading the file.")
