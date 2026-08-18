import hashlib
from copy import deepcopy
from typing import BinaryIO

import requests

from csfunctions.service.file_upload_schemas import PresignedWriteUrls


class PresignedUploadMixin:
    """
    Uploading content to presigned blob URLs, shared by all services that
    hand content to the blob storage directly.
    """

    def _upload_from_stream(
        self, presigned_urls: PresignedWriteUrls, stream: BinaryIO
    ) -> tuple[PresignedWriteUrls, str]:
        """Upload file stream in chunks and return updated presigned URLs and sha256 hash."""
        etags: list[str] = []
        sha256 = hashlib.sha256()
        for url in presigned_urls.urls:
            data: bytes = stream.read(presigned_urls.chunksize)
            sha256.update(data)
            resp = requests.put(url, data=data, headers=presigned_urls.headers, timeout=20)
            # 20 second timeout to stay below 30s max execution time of the Function
            # otherwise we won't get a proper error message in the logs
            resp.raise_for_status()
            etag = resp.headers.get("ETag")
            if etag:
                etags.append(etag)
        updated = deepcopy(presigned_urls)
        if etags:
            updated.etags = etags
        return updated, sha256.hexdigest()

    @staticmethod
    def _get_stream_size(stream: BinaryIO) -> int:
        """Get the size of a seekable stream."""
        if not stream.seekable():
            raise ValueError("Stream is not seekable; size cannot be determined.")
        current_pos = stream.tell()
        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(current_pos)
        return size
