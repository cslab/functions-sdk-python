from typing import Optional

import requests

from csfunctions.metadata import MetaData


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class Conflict(Exception):
    pass


class NotFound(Exception):
    pass


class UnprocessableEntity(Exception):
    pass


class RateLimitExceeded(Exception):
    pass


class BaseService:
    """
    Base class for services.
    """

    def __init__(self, metadata: MetaData):
        # Store full metadata for services that need additional fields (e.g. app_user)
        self.metadata = metadata

    def request(
        self, endpoint: str, method: str = "GET", params: Optional[dict] = None, json: Optional[dict] = None
    ) -> dict | list:
        """
        Make a request to the access service.
        """
        if self.metadata.service_url is None:
            raise ValueError("No service url given.")
        if self.metadata.service_token is None:
            raise ValueError("No service token given.")

        headers = {"Authorization": f"Bearer {self.metadata.service_token}"}
        params = params or {}
        url = str(self.metadata.service_url).rstrip("/") + "/" + endpoint.lstrip("/")
        response = requests.request(method, url=url, params=params, headers=headers, timeout=10, json=json)

        if response.status_code == 401:
            raise Unauthorized
        if response.status_code == 403:
            raise Forbidden
        elif response.status_code == 409:
            raise Conflict
        elif response.status_code == 404:
            raise NotFound
        elif response.status_code == 422:
            raise UnprocessableEntity(response.text)
        elif response.status_code == 429:
            raise RateLimitExceeded(response.text)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Access service responded with status code {response.status_code}.")
