import io
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests_mock

from csfunctions import MetaData, Service
from csfunctions.service.base import BaseService, Unauthorized
from csfunctions.service.file_upload import FileUploadService
from csfunctions.service.file_upload_schemas import PresignedWriteUrls


class TestNumberGeneratorService(TestCase):
    endpoint = "numgen"
    service_url = "https://some_service_url"
    service_token = "some_service_token"  # nosec
    service: Service

    @classmethod
    def setUpClass(cls) -> None:
        cls.endpoint = "numgen"
        cls.service_url = "https://some_service_url"
        cls.service_token = "some_service_token"  # nosec
        metadata = MetaData.model_validate(
            {
                "request_id": "req-1",
                "app_lang": "en",
                "app_user": "tester",
                "request_datetime": datetime(2000, 1, 1),
                "transaction_id": "txn-1",
                "instance_url": "https://instance.contact-cloud.com",
                "service_url": cls.service_url,
                "service_token": cls.service_token,
                "db_service_url": None,
            }
        )
        cls.service = Service(metadata=metadata)

    @requests_mock.Mocker()
    def test_get_number(self, mock_request: requests_mock.Mocker):
        mock_request.get(f"{self.service_url}/{self.endpoint}?name=test&count=1", text='{"numbers": [1,2,3]}')
        number = self.service.generator.get_number("test")
        last_request = mock_request.last_request
        self.assertIsNotNone(last_request)
        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {self.service_token}", last_request.headers["Authorization"])
        self.assertEqual(1, number)

    @requests_mock.Mocker()
    def test_get_numbers(self, mock_request: requests_mock.Mocker):
        mock_request.get(f"{self.service_url}/{self.endpoint}?name=test&count=3", text='{"numbers": [1,2,3]}')
        numbers = self.service.generator.get_numbers("test", 3)
        last_request = mock_request.last_request
        self.assertIsNotNone(last_request)
        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {self.service_token}", last_request.headers["Authorization"])
        self.assertEqual([1, 2, 3], numbers)


class TestBaseService(TestCase):
    @requests_mock.Mocker()
    def test_request(self, mock_request: requests_mock.Mocker):
        endpoint = "some_endpoint"
        service_url = "https://some_service_url"
        service_token = "some_service_token"  # nosec
        params = {"param1": 1, "param2": 2}

        mock_request.get(f"{service_url}/{endpoint}?param1=1&param2=2", text="{}")
        metadata = MetaData.model_validate(
            {
                "request_id": "req-1",
                "app_lang": "en",
                "app_user": "tester",
                "request_datetime": datetime(2000, 1, 1),
                "transaction_id": "txn-1",
                "instance_url": "https://instance.contact-cloud.com",
                "service_url": service_url,
                "service_token": service_token,
                "db_service_url": None,
            }
        )
        service = BaseService(metadata=metadata)

        response = service.request(endpoint, "GET", params)
        last_request = mock_request.last_request
        self.assertIsNotNone(last_request)
        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {service_token}", last_request.headers["Authorization"])
        self.assertEqual({}, response)

        # test unauthorized
        mock_request.get(f"{service_url}/{endpoint}?param1=1&param2=2", status_code=401)
        with self.assertRaises(Unauthorized):
            service.request(endpoint, "GET", params)

        # test server error
        mock_request.get(f"{service_url}/{endpoint}?param1=1&param2=2", status_code=500)
        with self.assertRaises(ValueError):
            service.request(endpoint, "GET", params)

        # test no params
        mock_request.get(f"{service_url}/{endpoint}", text="{}")
        response = service.request(endpoint, "GET")
        last_request = mock_request.last_request
        self.assertIsNotNone(last_request)
        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {service_token}", last_request.headers["Authorization"])
        self.assertEqual({}, response)


class TestFileUploadService(TestCase):
    def setUp(self):
        self.metadata = MetaData.model_validate(
            {
                "request_id": "req-1",
                "app_lang": "en",
                "app_user": "tester",
                "request_datetime": datetime(2000, 1, 1),
                "transaction_id": "txn-1",
                "instance_url": "https://instance.contact-cloud.com",
                "service_url": "https://some_service_url",
                "service_token": "some_service_token",
                "db_service_url": None,
            }
        )
        self.service = FileUploadService(metadata=self.metadata)

    def test_create_new_file(self):
        # Patch self.service.request to return a valid response
        with patch.object(self.service, "request", return_value={"file_object_id": "file123"}) as mock_request:
            file_id = self.service._create_new_file("test.txt", "parent1", "tester")
            self.assertEqual(file_id, "file123")
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertIn("endpoint", kwargs)
            self.assertEqual(kwargs["endpoint"], "/file_upload/create")
            self.assertEqual(kwargs["method"], "POST")
            self.assertIn("json", kwargs)
            self.assertEqual(kwargs["json"]["filename"], "test.txt")
            self.assertEqual(kwargs["json"]["parent_object_id"], "parent1")

    def test_get_presigned_write_urls(self):
        mock_response = {
            "blob_id": "blob123",
            "urls": ["https://upload.url/1", "https://upload.url/2"],
            "chunksize": 1024,
            "headers": {"Authorization": "Bearer token"},
        }
        with patch.object(self.service, "request", return_value=mock_response) as mock_request:
            result = self.service._get_presigned_write_urls("file123", 2048, "lockid", "tester")
            self.assertEqual(result.blob_id, "blob123")
            self.assertEqual(result.chunksize, 1024)
            self.assertEqual(result.urls, ["https://upload.url/1", "https://upload.url/2"])
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertIn("endpoint", kwargs)
            self.assertTrue("generate_presigned_url" in kwargs["endpoint"])
            self.assertEqual(kwargs["method"], "POST")
            self.assertEqual(kwargs["json"]["filesize"], 2048)
            self.assertEqual(kwargs["json"]["lock_id"], "lockid")

    def test_upload_from_stream(self):
        # Test with multiple URLs and ETags
        presigned = PresignedWriteUrls(
            blob_id="blob123",
            urls=["https://upload.url/1", "https://upload.url/2"],
            chunksize=2,
            headers={"Authorization": "Bearer token"},
        )
        # Simulate a file-like object with 4 bytes, so 2 chunks
        stream = io.BytesIO(b"abcd")
        # Each call to requests.put returns a different ETag
        mock_response1 = MagicMock()
        mock_response1.headers = {"ETag": "etag1"}
        mock_response1.raise_for_status = MagicMock()
        mock_response2 = MagicMock()
        mock_response2.headers = {"ETag": "etag2"}
        mock_response2.raise_for_status = MagicMock()
        with patch("requests.put", side_effect=[mock_response1, mock_response2]) as mock_put:
            updated, sha256 = self.service._upload_from_stream(presigned, stream)
            self.assertEqual(updated.etags, ["etag1", "etag2"])
            self.assertEqual(len(sha256), 64)  # sha256 hex length
            import hashlib

            expected_hash = hashlib.sha256(b"abcd").hexdigest()
            self.assertEqual(sha256, expected_hash)
            self.assertEqual(mock_put.call_count, 2)
            # Check each call
            call_args_list = mock_put.call_args_list
            self.assertEqual(call_args_list[0][0][0], "https://upload.url/1")
            self.assertEqual(call_args_list[0][1]["data"], b"ab")
            self.assertEqual(call_args_list[1][0][0], "https://upload.url/2")
            self.assertEqual(call_args_list[1][1]["data"], b"cd")
            for call_args in call_args_list:
                self.assertEqual(call_args[1]["headers"], {"Authorization": "Bearer token"})

    def test_get_stream_size(self):
        stream = io.BytesIO(b"abcde")
        size = self.service._get_stream_size(stream)
        self.assertEqual(size, 5)
        # Check that stream position is unchanged
        self.assertEqual(stream.tell(), 0)

    def test_complete_upload(self):
        presigned = PresignedWriteUrls(
            blob_id="blob123", urls=["https://upload.url/1"], chunksize=4, headers={"Authorization": "Bearer token"}
        )
        with patch.object(self.service, "request", return_value=None) as mock_request:
            self.service._complete_upload(
                file_object_id="file123",
                filesize=4,
                lock_id="lockid",
                presigned_urls=presigned,
                persno="tester",
                sha256="deadbeef",
            )
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertIn("endpoint", kwargs)
            self.assertTrue("complete" in kwargs["endpoint"])
            self.assertEqual(kwargs["method"], "POST")
            self.assertEqual(kwargs["json"].get("file_object_id", "file123"), "file123")
            self.assertEqual(kwargs["json"]["sha256"], "deadbeef")

    def test_upload_new_file(self):
        # Patch _create_new_file and upload_file_content
        with (
            patch.object(self.service, "_create_new_file", return_value="file123") as mock_create,
            patch.object(self.service, "upload_file_content", return_value=None) as mock_upload,
        ):
            stream = io.BytesIO(b"abc")
            file_id = self.service.upload_new_file("parent1", "test.txt", stream)
            self.assertEqual(file_id, "file123")
            mock_create.assert_called_once_with(
                filename="test.txt",
                parent_object_id="parent1",
                persno="tester",
                check_access=True,
            )
            mock_upload.assert_called_once()
            args, kwargs = mock_upload.call_args
            self.assertEqual(kwargs["file_object_id"], "file123")
            self.assertEqual(kwargs["stream"].getvalue(), b"abc")

    def test_upload_file_content(self):
        # Patch internal methods to isolate upload_file_content logic
        with (
            patch.object(self.service, "_get_stream_size", return_value=4) as mock_size,
            patch.object(self.service, "_get_presigned_write_urls") as mock_presigned,
            patch.object(self.service, "_upload_from_stream") as mock_upload,
            patch.object(self.service, "_complete_upload") as mock_complete,
        ):
            # Setup mocks
            mock_presigned.return_value = PresignedWriteUrls(
                blob_id="blob123",
                urls=["https://upload.url/1", "https://upload.url/2"],
                chunksize=2,
                headers={"Authorization": "Bearer token"},
            )
            mock_upload.return_value = (
                PresignedWriteUrls(
                    blob_id="blob123",
                    urls=["https://upload.url/1", "https://upload.url/2"],
                    chunksize=2,
                    headers={"Authorization": "Bearer token"},
                    etags=["etag1", "etag2"],
                ),
                "deadbeef",
            )
            stream = io.BytesIO(b"abcd")
            # Call method
            self.service.upload_file_content(
                file_object_id="file123",
                stream=stream,
                persno="tester",
                check_access=True,
                filesize=None,
                delete_derived_files=False,
            )
            mock_size.assert_called_once_with(stream)
            mock_presigned.assert_called_once_with(
                file_object_id="file123",
                filesize=4,
                lock_id=mock_presigned.call_args[1]["lock_id"],
                persno="tester",
                check_access=True,
            )
            mock_upload.assert_called_once_with(presigned_urls=mock_presigned.return_value, stream=stream)
            mock_complete.assert_called_once()
            args, kwargs = mock_complete.call_args
            self.assertEqual(kwargs["file_object_id"], "file123")
            self.assertEqual(kwargs["filesize"], 4)
            self.assertEqual(kwargs["presigned_urls"].etags, ["etag1", "etag2"])
            self.assertEqual(kwargs["persno"], "tester")
            self.assertEqual(kwargs["sha256"], "deadbeef")
            self.assertEqual(kwargs["delete_derived_files"], False)

    def test_abort_upload(self):
        presigned = PresignedWriteUrls(
            blob_id="blob123",
            urls=["https://upload.url/1"],
            chunksize=4,
            headers={"Authorization": "Bearer token"},
        )
        with patch.object(self.service, "request", return_value=None) as mock_request:
            self.service._abort_upload(
                file_object_id="file123",
                lock_id="lockid",
                persno="tester",
                presigned_write_urls=presigned,
            )
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertIn("endpoint", kwargs)
            self.assertTrue("abort" in kwargs["endpoint"])
            self.assertEqual(kwargs["method"], "POST")
            self.assertEqual(kwargs["json"]["lock_id"], "lockid")
            self.assertEqual(kwargs["json"]["persno"], "tester")
            self.assertEqual(kwargs["json"]["presigned_write_urls"], presigned.model_dump())

    def test_upload_file_content_aborts_on_error(self):
        # Patch internal methods to simulate error and check abort
        with (
            patch.object(self.service, "_get_stream_size", return_value=4),
            patch.object(self.service, "_get_presigned_write_urls") as mock_presigned,
            patch.object(self.service, "_upload_from_stream", side_effect=Exception("upload error")),
            patch.object(self.service, "_abort_upload") as mock_abort,
        ):
            mock_presigned.return_value = PresignedWriteUrls(
                blob_id="blob123",
                urls=["https://upload.url/1", "https://upload.url/2"],
                chunksize=2,
                headers={"Authorization": "Bearer token"},
            )
            stream = io.BytesIO(b"abcd")
            with self.assertRaises(Exception) as cm:
                self.service.upload_file_content(
                    file_object_id="file123",
                    stream=stream,
                    persno="tester",
                    check_access=True,
                    filesize=None,
                    delete_derived_files=False,
                )
            self.assertEqual(str(cm.exception), "upload error")
            mock_abort.assert_called_once()
            args, kwargs = mock_abort.call_args
            self.assertEqual(kwargs["file_object_id"], "file123")
            self.assertEqual(kwargs["persno"], "tester")
            self.assertEqual(kwargs["presigned_write_urls"], mock_presigned.return_value)
