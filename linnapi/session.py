"""Session manager for the Linnworks API."""

from pathlib import Path
from typing import Any, Callable, MutableMapping, Optional, Union

import requests
import toml

from . import exceptions


class LinnworksAPISession:
    """Session manager for the Linnworks API."""

    application_id = None
    application_secret = None
    application_token = None
    session_token = None

    session = requests.Session()

    AUTH_URL = "https://api.linnworks.net/api/Auth/AuthorizeByApplication"

    CONFIG_FILENAME = ".linnapi.toml"

    def __enter__(self) -> requests.Session:
        if not self.__class__.credentials_are_set():
            config_path = self.__class__.find_config_filepath()
            if config_path is not None:
                self.__class__.load_from_config_file(config_file_path=config_path)
        if not self.__class__.credentials_are_set():
            raise exceptions.LoginCredentialsNotSetError()
        self.__class__._authorise_session()
        return self.__class__.session

    def __exit__(self, exc_type: None, exc_value: None, exc_tb: None) -> None:
        self.__class__.session

    @classmethod
    def set_login(
        cls,
        application_id: Optional[str] = None,
        application_secret: Optional[str] = None,
        application_token: Optional[str] = None,
    ) -> None:
        """Set login credentials (application_id, application_secret, application_token)."""
        cls.application_id = application_id
        cls.application_secret = application_secret
        cls.application_token = application_token

    @classmethod
    def credentials_are_set(cls) -> bool:
        """Return True if all auth credentials are set, otherwise False."""
        if None in (cls.application_id, cls.application_secret, cls.application_token):
            return False
        else:
            return True

    @classmethod
    def request_headers(cls) -> MutableMapping[str, str]:
        """Return request auth headers."""
        if cls.session_token is None:
            raise exceptions.SessionNotAuthorizedError()
        return {"Authorization": str(cls.session_token)}

    @classmethod
    def find_config_filepath(cls) -> Optional[Path]:
        """
        Return the path to a shopify config file or None.

        Recursivly scan backwards from the current working directory and return the
        path to a file matching cls.CONFIG_FILENAME if one exists, otherwise returns
        None.
        """
        path = Path.cwd()
        while path.parent != path:
            config_file = path / cls.CONFIG_FILENAME
            if config_file.exists():
                return config_file
            path = path.parent
        return None

    @classmethod
    def load_from_config_file(cls, config_file_path: Union[Path, str]) -> None:
        """Set login credentials as specified in a toml file located at config_file_path."""
        with open(config_file_path) as f:
            config = toml.load(f)
        cls.set_login(
            application_id=config.get("APPLICATION_ID"),
            application_secret=config.get("APPLICATION_SECRET"),
            application_token=config.get("APPLICATION_TOKEN"),
        )

    @classmethod
    def _authorise_session(cls) -> str:
        auth_request_data = {
            "ApplicationID": cls.application_id,
            "ApplicationSecret": cls.application_secret,
            "Token": cls.application_token,
        }
        auth_request_response = cls.session.post(cls.AUTH_URL, data=auth_request_data)
        auth_request_response.raise_for_status()
        cls.session_token = str(auth_request_response.json()["Token"])
        return cls.session_token


def linnworks_api_session(func: Callable) -> Callable:
    """Use a Linnworks API session as a method decorator."""

    def wrapper_linnapi_session(*args: Any, **kwargs: Any) -> Any:
        with LinnworksAPISession():
            return func(*args, **kwargs)

    return wrapper_linnapi_session
