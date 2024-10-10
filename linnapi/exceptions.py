"""Exceptions for the linnapi package."""

from typing import Any, Mapping


class LoginCredentialsNotSetError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when creating an API session without credentials set."""
        super().__init__(
            "APPLICATION_ID, APPLICATION_SECRET and APPLICATION_TOKEN must be set."
        )


class SessionNotAuthorizedError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when making a request without a session token."""
        super().__init__("Request session must be authorized.")


class InvalidResponseError(ValueError):
    """Exception raised wthen and API request returns an invalid response."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Exception raised wthen and API request returns an invalid response."""
        super().__init__(*args, **kwargs)


class IncompleteResponseError(ValueError):
    """Exception raised wthen and API request returns a response with missing data."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Exception raised wthen and API request returns a response with missing data."""
        super().__init__(*args, **kwargs)
