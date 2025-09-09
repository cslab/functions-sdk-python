from typing import Optional

from pydantic import BaseModel, Field


class PresignedWriteUrls(BaseModel):
    """
    Context object for managing upload information.
    """

    blob_id: str
    urls: list[str]
    chunksize: int
    upload_id: Optional[str] = None
    etags: Optional[list[str]] = None
    block_ids: Optional[list[str]] = None
    headers: Optional[dict[str, str]] = None
    metadata: Optional[dict[str, str]] = None
    signature: Optional[str] = None


class GeneratePresignedUrlRequest(BaseModel):
    """
    Response model for generating presigned URLs.
    """

    filesize: int = Field(..., description="The size of the file you want to upload in bytes.", ge=0)
    check_access: bool = Field(..., description="Whether to check access permissions.")
    persno: str = Field(..., description="The persno of the user who is uploading the file.")
    lock_id: str = Field(..., description="Provide some random string to lock the file for upload.")


class CompleteFileUploadRequest(BaseModel):
    """
    Request model for completing a file upload.
    """

    filesize: int = Field(..., description="The size of the file you want to upload in bytes.", ge=0)
    check_access: bool = Field(..., description="Whether to check access permissions.")
    persno: str = Field(..., description="The persno of the user who is uploading the file.")
    presigned_write_urls: PresignedWriteUrls = Field(..., description="The presigned write URLs for the file upload.")
    sha256: Optional[str] = Field(None, description="The SHA256 hash of the file content.")
    lock_id: str = Field(..., description="The lock ID the file was locked with")
    delete_derived_files: bool = Field(True, description="Whether to delete derived files (e.g. converted pdfs).")


class AbortFileUploadRequest(BaseModel):
    """
    Request model for aborting a file upload.
    """

    presigned_write_urls: PresignedWriteUrls = Field(..., description="The presigned write URLs for the file upload.")
    lock_id: str = Field(..., description="The lock ID the file was locked with")
    persno: str = Field(..., description="The persno of the user who is uploading the file.")


class CreateNewFileRequest(BaseModel):
    """
    Request model for creating a new file.
    """

    parent_object_id: str = Field(..., description="cdb_object_id of the object the file should be attached to.")
    filename: str = Field(..., description="The name of the file to create.")
    persno: str = Field(..., description="The persno of the user creating the file.")
    check_access: bool = Field(..., description="Whether to check access permissions.")


class CreateNewFileResponse(BaseModel):
    """
    Response model for creating a new file.
    """

    file_object_id: str = Field(..., description="The cdb_object_id of the newly created file.")
