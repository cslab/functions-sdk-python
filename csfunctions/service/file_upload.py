from random import choice
from string import ascii_letters
from typing import BinaryIO

from csfunctions.service.base import BaseService
from csfunctions.service.file_upload_schemas import (
    AbortFileUploadRequest,
    CompleteFileUploadRequest,
    CreateNewFileRequest,
    CreateNewFileResponse,
    GeneratePresignedUrlRequest,
    PresignedWriteUrls,
)
from csfunctions.service.presigned_upload import PresignedUploadMixin


def _generate_lock_id():
    """Generate a random 12-character lock ID."""
    return "".join(choice(ascii_letters) for i in range(12))  # nosec


class FileUploadService(PresignedUploadMixin, BaseService):
    def _create_new_file(self, filename: str, parent_object_id: str, persno: str, check_access: bool = True) -> str:
        """Create a new empty file attached to the parent object."""
        response_json = self.request(
            endpoint="/file_upload/create",
            method="POST",
            json=CreateNewFileRequest(
                parent_object_id=parent_object_id, filename=filename, persno=persno, check_access=check_access
            ).model_dump(),
        )
        data = CreateNewFileResponse.model_validate(response_json)
        return data.file_object_id

    def _get_presigned_write_urls(
        self, file_object_id: str, filesize: int, lock_id: str, persno: str, check_access: bool = True
    ) -> PresignedWriteUrls:
        """Request presigned URLs for uploading file chunks."""
        response_json = self.request(
            endpoint=f"/file_upload/{file_object_id}/generate_presigned_url",
            method="POST",
            json=GeneratePresignedUrlRequest(
                check_access=check_access, persno=persno, filesize=filesize, lock_id=lock_id
            ).model_dump(),
        )

        return PresignedWriteUrls.model_validate(response_json)

    def _complete_upload(
        self,
        file_object_id: str,
        filesize: int,
        lock_id: str,
        presigned_urls: PresignedWriteUrls,
        persno: str,
        check_access: bool = True,
        sha256: str | None = None,
        delete_derived_files: bool = True,
    ) -> None:
        """Mark the upload as complete and finalize the file."""
        self.request(
            endpoint=f"/file_upload/{file_object_id}/complete",
            method="POST",
            json=CompleteFileUploadRequest(
                filesize=filesize,
                check_access=check_access,
                persno=persno,
                presigned_write_urls=presigned_urls,
                lock_id=lock_id,
                sha256=sha256,
                delete_derived_files=delete_derived_files,
            ).model_dump(),
        )

    def _abort_upload(
        self, file_object_id: str, lock_id: str, persno: str, presigned_write_urls: PresignedWriteUrls
    ) -> None:
        """Abort an ongoing file upload."""
        self.request(
            endpoint=f"/file_upload/{file_object_id}/abort",
            method="POST",
            json=AbortFileUploadRequest(
                lock_id=lock_id,
                persno=persno,
                presigned_write_urls=presigned_write_urls,
            ).model_dump(),
        )

    def upload_file_content(
        self,
        file_object_id: str,
        stream: BinaryIO,
        persno: str | None = None,
        check_access: bool = True,
        filesize: int | None = None,
        delete_derived_files: bool = True,
    ) -> None:
        """
        Uploads content to an existing file object in chunks using presigned URLs.
        Handles aborting the upload if an error occurs.

        Args:
            file_object_id: The ID of the file object to upload to.
            stream: A binary stream containing the file data.
            persno: The user/person number who is uploading the file (default is user that triggered the Function).
            check_access: Whether to check access permissions.
            filesize: Size of the file in bytes (required only if the stream is not seekable).
            delete_derived_files: Whether to delete derived files after upload.

        Raises:
            csfunctions.service.Forbidden: If access check fails.
            csfunctions.service.Unauthorized: If the service token is invalid.
            csfunctions.service.Conflict: If the file is already locked.
            csfunctions.service.NotFound: If the file object does not exist.
            csfunctions.service.RateLimitExceeded: If the services rate limit is exceeded.
        """
        persno = persno or self.metadata.app_user
        if filesize is None:
            filesize = self._get_stream_size(stream)
        lock_id = _generate_lock_id()
        presigned = self._get_presigned_write_urls(
            file_object_id=file_object_id,
            filesize=filesize,
            lock_id=lock_id,
            persno=persno,
            check_access=check_access,
        )
        try:
            presigned_with_etags, sha256 = self._upload_from_stream(presigned_urls=presigned, stream=stream)
            self._complete_upload(
                file_object_id=file_object_id,
                filesize=filesize,
                lock_id=lock_id,
                presigned_urls=presigned_with_etags,
                persno=persno,
                check_access=check_access,
                sha256=sha256,
                delete_derived_files=delete_derived_files,
            )
        except Exception as e:
            # if something goes wrong during upload we try to abort
            self._abort_upload(
                file_object_id=file_object_id,
                lock_id=lock_id,
                persno=persno,
                presigned_write_urls=presigned,
            )
            raise e

    def upload_new_file(
        self,
        parent_object_id: str,
        filename: str,
        stream: BinaryIO,
        persno: str | None = None,
        check_access: bool = True,
        filesize: int | None = None,
    ) -> str:
        """
        Creates a new file attached to the parent object and uploads content from the provided stream.

        Args:
            parent_object_id: The ID of the parent object to attach the file to.
            filename: The name of the new file.
            stream: A binary stream containing the file data.
            persno: The user/person number who is uploading the file (default is user that triggered the Function).
            check_access: Whether to check access permissions.
            filesize: Size of the file in bytes (required only if the stream is not seekable).

        Returns:
            The ID of the newly created file object.

        Raises:
            csfunctions.service.Forbidden: If access check fails.
            csfunctions.service.Unauthorized: If the service token is invalid.
            csfunctions.service.NotFound: If the parent object does not exist.
            csfunctions.service.RateLimitExceeded: If the services rate limit is exceeded.
        """
        persno = persno or self.metadata.app_user
        file_object_id = self._create_new_file(
            filename=filename,
            parent_object_id=parent_object_id,
            persno=persno,
            check_access=check_access,
        )
        self.upload_file_content(
            file_object_id=file_object_id,
            stream=stream,
            persno=persno,
            check_access=check_access,
            filesize=filesize,
            delete_derived_files=False,
        )
        return file_object_id
