import hashlib
import hmac
import json
import time
from unittest import TestCase
from unittest.mock import MagicMock, patch

from werkzeug.datastructures import Headers
from werkzeug.wrappers import Request

from csfunctions.devserver import _is_error_response, _verify_hmac_signature, handle_request
from csfunctions.handler import FunctionNotRegistered


class TestDevServer(TestCase):
    def setUp(self):
        self.secret_token = "test-secret-token"  # nosec: B105
        self.function_name = "test-function"
        self.request_body = "test-body"
        self.timestamp = str(int(time.time()))
        self.signature = hmac.new(
            self.secret_token.encode("utf-8"),
            f"{self.timestamp}{self.request_body}".encode(),
            hashlib.sha256,
        ).hexdigest()

    def create_request(self, path="/test-function", body="test-body", signature=None, timestamp=None):
        environ = {
            "PATH_INFO": path,
            "wsgi.input": MagicMock(),
            "REQUEST_METHOD": "POST",
        }
        request = Request(environ)
        request.get_data = MagicMock(return_value=body)

        if signature:
            request.headers = Headers({"X-CON-Signature-256": signature, "X-CON-Timestamp": timestamp})
        return request

    def test_handle_request_no_function_name(self):
        """Test handling request with no function name"""
        request = self.create_request(path="/")
        response = handle_request(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "No function name provided")

    @patch("csfunctions.devserver.execute")
    @patch.dict("os.environ", {"CFC_SECRET_TOKEN": ""})
    def test_handle_request_success(self, mock_execute):
        """Test successful request handling"""
        expected_response = {"result": "success"}
        mock_execute.return_value = json.dumps(expected_response)

        request = self.create_request()
        response = handle_request(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(json.loads(response.get_data(as_text=True)), expected_response)

    @patch("csfunctions.devserver.execute")
    @patch.dict("os.environ", {"CFC_SECRET_TOKEN": ""})
    def test_handle_request_function_not_registered(self, mock_execute):
        """Test handling of non-existent function"""
        mock_execute.side_effect = FunctionNotRegistered("Function not found")

        request = self.create_request()
        response = handle_request(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), "Function not found")

    @patch("csfunctions.devserver.execute")
    @patch.dict("os.environ", {"CFC_SECRET_TOKEN": ""})
    def test_handle_request_error_response(self, mock_execute):
        """Test handling of error response from function"""
        error_response = {"response_type": "error", "message": "Something went wrong"}
        mock_execute.return_value = json.dumps(error_response)

        request = self.create_request()
        response = handle_request(request)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(json.loads(response.get_data(as_text=True)), error_response)

    def test_verify_hmac_signature_valid(self):
        """Test HMAC signature verification with valid signature"""
        result = _verify_hmac_signature(self.signature, self.timestamp, self.request_body, self.secret_token)
        self.assertTrue(result)

    def test_verify_hmac_signature_invalid(self):
        """Test HMAC signature verification with invalid signature"""
        result = _verify_hmac_signature("invalid-signature", self.timestamp, self.request_body, self.secret_token)
        self.assertFalse(result)

    def test_verify_hmac_signature_expired(self):
        """Test HMAC signature verification with expired timestamp"""
        old_timestamp = str(int(time.time()) - 120)  # 2 minutes old
        result = _verify_hmac_signature(self.signature, old_timestamp, self.request_body, self.secret_token)
        self.assertFalse(result)

    def test_is_error_response(self):
        """Test error response detection"""
        # Test string response
        self.assertFalse(_is_error_response("not an error"))

        # Test JSON string response
        error_response = json.dumps({"response_type": "error"})
        self.assertTrue(_is_error_response(error_response))

        # Test dict response
        self.assertTrue(_is_error_response({"response_type": "error"}))
        self.assertFalse(_is_error_response({"response_type": "success"}))

        # Test invalid JSON string
        self.assertFalse(_is_error_response("{invalid json}"))
