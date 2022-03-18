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
        print(response.json())
        return response.json()


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
