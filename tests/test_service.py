from unittest import TestCase

import requests_mock

from csfunctions import Service
from csfunctions.service import BaseService, Unauthorized


class TestNumberGeneratorService(TestCase):
    endpoint = "numgen"
    service_url = "https://some_service_url"
    service_token = "some_service_token"  # nosec
    service: Service

    @classmethod
    def setUpClass(cls) -> None:
        cls.service = Service(cls.service_url, cls.service_token)

    @requests_mock.Mocker()
    def test_get_number(self, mock_request: requests_mock.Mocker):
        mock_request.get(f"{self.service_url}/{self.endpoint}?name=test&count=1", text='{"numbers": [1,2,3]}')

        number = self.service.generator.get_number("test")
        last_request = mock_request.last_request

        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {self.service_token}", last_request.headers["Authorization"])
        self.assertEqual(1, number)

    @requests_mock.Mocker()
    def test_get_numbers(self, mock_request: requests_mock.Mocker):
        mock_request.get(f"{self.service_url}/{self.endpoint}?name=test&count=3", text='{"numbers": [1,2,3]}')

        numbers = self.service.generator.get_numbers("test", 3)
        last_request = mock_request.last_request

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
        service = BaseService(service_url, service_token)

        response = service.request(endpoint, "GET", params)
        last_request = mock_request.last_request
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
        self.assertEqual("GET", last_request.method)
        self.assertEqual(f"Bearer {service_token}", last_request.headers["Authorization"])
        self.assertEqual({}, response)
