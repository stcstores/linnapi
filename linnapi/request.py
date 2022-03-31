"""Methods for making Linnworks API requests."""

from typing import Any, MutableMapping, Type

import requests

from .session import LinnworksAPISession


class LinnworksAPIRequest:
    """Base class for Linnworks API requests."""

    URL = ""

    GET = "GET"
    POST = "POST"

    METHOD = GET

    @classmethod
    def headers(cls, *args: Any, **kwargs: Any) -> MutableMapping[str, str]:
        """Return request headers."""
        return {}

    @classmethod
    def params(cls, *args: Any, **kwargs: Any) -> None | dict[str, Any]:
        """Return request URL parameters."""
        return None

    @classmethod
    def data(cls, *args: Any, **kwargs: Any) -> None | dict[str, Any]:
        """Return request POST data."""
        return None

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> None | dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        return None

    @classmethod
    def parse_response(
        cls, response: requests.models.Response, *args: Any, **kwargs: Any
    ) -> Any:
        """Parse the request response."""
        return response.json()

    @classmethod
    def multi_headers(
        cls, requests: list[MutableMapping[str, Any]]
    ) -> MutableMapping[str, str]:
        """Return request headers."""
        return cls.headers(requests[0])

    @classmethod
    def multi_params(
        cls, requests: list[MutableMapping[str, Any]]
    ) -> None | dict[str, Any]:
        """Return request URL parameters."""
        return cls.params(requests[0])

    @classmethod
    def multi_data(
        cls, requests: list[MutableMapping[str, Any]]
    ) -> None | dict[str, Any]:
        """Return request POST data."""
        return cls.data(requests[0])

    @classmethod
    def multi_json(
        cls, requests: list[MutableMapping[str, Any]]
    ) -> None | dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        return cls.json(requests[0])

    @classmethod
    def multi_parse_response(
        cls,
        response: requests.models.Response,
        requests: list[MutableMapping[str, Any]],
    ) -> Any:
        """Parse the request response."""
        return cls.parse_response(response, requests[0])


class MultiItemRequest:
    """Base class for multi-item requesters."""

    request_method = LinnworksAPIRequest

    def __init__(self) -> None:
        """Create a request with multiple repeated parameters."""
        self.requests: list[MutableMapping[str, Any]] = []

    def _add_request(self, request: MutableMapping[str, Any]) -> None:
        self.requests.append(request)

    def add_request(self, *args: Any, **kwargs: Any) -> None:
        """Add a request to the request list."""
        raise NotImplementedError

    def request(self) -> Any:
        """Make request with added parameters."""
        headers = LinnworksAPISession.request_headers()
        headers.update(self.request_method.multi_headers(self.requests))
        params = self.request_method.multi_params(self.requests)
        data = self.request_method.multi_data(self.requests)
        json = self.request_method.multi_json(self.requests)
        response = LinnworksAPISession.session.request(
            url=self.request_method.URL,
            method=self.request_method.METHOD,
            headers=headers,
            params=params,
            data=data,
            json=json,
        )
        return self.request_method.multi_parse_response(response, self.requests)


def make_request(
    request_method: Type[LinnworksAPIRequest], *args: Any, **kwargs: Any
) -> Any:
    """Make a Linnworks API request."""
    headers = LinnworksAPISession.request_headers()
    headers.update(request_method.headers(*args, **kwargs))
    params = request_method.params(*args, **kwargs)
    data = request_method.data(*args, **kwargs)
    json = request_method.json(*args, **kwargs)
    response = LinnworksAPISession.session.request(
        url=request_method.URL,
        method=request_method.METHOD,
        headers=headers,
        params=params,
        data=data,
        json=json,
    )
    return request_method.parse_response(response, *args, **kwargs)
