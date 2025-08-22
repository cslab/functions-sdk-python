from typing import Optional

import requests


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
