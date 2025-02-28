from typing import Optional

import requests


class Service:
    """
    Provides access to services on the elements instance, e.g. generating numbers.
    """

    def __init__(self, service_url: str | None, service_token: str | None):
        self.generator = NumberGeneratorService(service_url, service_token)


class Unauthorized(Exception):
    pass


class BaseService:
    """
    Base class for services.
    """

    def __init__(self, service_url: str | None, service_token: str | None):
        self.service_url = service_url
        self.service_token = service_token

    def request(self, endpoint: str, method: str = "GET", params: Optional[dict] = None) -> dict | list:
        """
        Make a request to the access service.
        """
        if self.service_url is None:
            raise ValueError("No service url given.")
        if self.service_token is None:
            raise ValueError("No service token given.")

        headers = {"Authorization": f"Bearer {self.service_token}"}
        params = params or {}
        url = self.service_url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = requests.request(method, url=url, params=params, headers=headers, timeout=10)

        if response.status_code == 401:
            raise Unauthorized
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Access service responded with status code {response.status_code}.")


class NumberGeneratorService(BaseService):
    """
    Service for generating numbers in the elements instance.
    """

    endpoint = "/numgen"

    def get_number(self, name: str) -> int:
        """
        Retrieve one number from the given generator.

        Hint: If you need more than one number use the get_numbers method instead,
        to retrieve multiple numbers in one request to the elements instance.

        :param name: name of the generator
        :return: generated number
        """
        numbers = self.get_numbers(name, 1)
        return numbers[0]

    def get_numbers(self, name: str, count: int) -> list[int]:
        """
        Retrieve multiple numbers from the given generator.

        If you need more than one number this function is more efficient to use than making multiple calls
        to get_number, because this method only performs one request to the elements instance.

        :param name: name of the generator
        :param count:  how many numbers should be generated
        :return: list of generated numbers
        """
        params = {"name": name, "count": count}
        data = self.request(self.endpoint, params=params)
        if not isinstance(data, dict):
            raise ValueError(f"Access service returned invalid data. Expected dict, got {type(data)}")
        if "numbers" not in data:
            raise ValueError(f"Access service returned invalid data. Expected 'numbers' key, got {data.keys()}")
        return data["numbers"]
