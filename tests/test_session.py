from pathlib import Path

import pytest
import requests
import toml

from linnapi import exceptions, session


@pytest.fixture(autouse=True)
def temp_cwd(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


@pytest.fixture
def application_id():
    return "mock-application-id"


@pytest.fixture
def application_secret():
    return "mock-application-secret"


@pytest.fixture
def application_token():
    return "mock-application-token"


@pytest.fixture
def session_token():
    return "mock-session-token"


@pytest.fixture
def auth_request_response(session_token):
    return {"Token": session_token}


@pytest.fixture(autouse=True)
def clean_linnworks_api_session():
    yield
    session.LinnworksAPISession.application_id = None
    session.LinnworksAPISession.application_secret = None
    session.LinnworksAPISession.application_token = None
    session.LinnworksAPISession.session_token = None
    session.LinnworksAPISession.session = requests.Session()
    session.LinnworksAPISession.CONFIG_FILENAME = ".linnapi.toml"


@pytest.fixture
def set_linnworks_session_config(application_id, application_secret, application_token):
    session.LinnworksAPISession.application_id = application_id
    session.LinnworksAPISession.application_secret = application_secret
    session.LinnworksAPISession.application_token = application_token


@pytest.fixture
def config_file(application_id, application_secret, application_token):
    data = {
        "APPLICATION_ID": application_id,
        "APPLICATION_SECRET": application_secret,
        "APPLICATION_TOKEN": application_token,
    }
    path = Path.cwd() / session.LinnworksAPISession.CONFIG_FILENAME
    with open(path, "w") as f:
        toml.dump(data, f)
    return path


@pytest.fixture
def mock_auth_request(requests_mock, auth_request_response):
    requests_mock.post(session.LinnworksAPISession.AUTH_URL, json=auth_request_response)
    return requests_mock


@pytest.mark.parametrize(
    "application_id_set,application_secret_set,application_token_set,expected",
    [
        (False, False, False, False),
        (False, False, True, False),
        (False, True, False, False),
        (True, False, False, False),
        (True, True, False, False),
        (True, False, True, False),
        (False, True, True, False),
        (True, True, True, True),
    ],
)
def test_credentials_are_set_method(
    application_id,
    application_secret,
    application_token,
    application_id_set,
    application_secret_set,
    application_token_set,
    expected,
):
    if application_id_set is True:
        session.LinnworksAPISession.application_id = application_id
    else:
        session.LinnworksAPISession.application_id = None
    if application_secret_set is True:
        session.LinnworksAPISession.application_secret = application_secret
    else:
        session.LinnworksAPISession.application_secret = None
    if application_token_set is True:
        session.LinnworksAPISession.application_token = application_token
    else:
        session.LinnworksAPISession.application_token = None
    assert session.LinnworksAPISession.credentials_are_set() is expected


def test_raises_exception_when_called_without_credentials(requests_mock):
    with pytest.raises(exceptions.LoginCredentialsNotSetError):
        with session.LinnworksAPISession():
            pass


def test_request_headers_raises_if_session_token_not_set():
    with pytest.raises(exceptions.SessionNotAuthorizedError):
        session.LinnworksAPISession.request_headers()


def test_request_headers_returns_request_headers(session_token):
    session.LinnworksAPISession.session_token = session_token
    expected_response = {"Authorization": session_token}
    assert session.LinnworksAPISession.request_headers() == expected_response


def test_authorise_session_makes_auth_request(
    mock_auth_request, auth_request_response, set_linnworks_session_config
):
    session.LinnworksAPISession._authorise_session()
    request = mock_auth_request.request_history[0]
    assert request.method == "POST"
    assert request.url == session.LinnworksAPISession.AUTH_URL
    assert request.text == (
        f"ApplicationID={session.LinnworksAPISession.application_id}&"
        f"ApplicationSecret={session.LinnworksAPISession.application_secret}&"
        f"Token={session.LinnworksAPISession.application_token}"
    )


def test_authorise_session_sets_session_token(
    mock_auth_request,
    auth_request_response,
    set_linnworks_session_config,
    session_token,
):
    session.LinnworksAPISession._authorise_session()
    assert session.LinnworksAPISession.session_token == session_token


def test_authorise_session_returns_session_token(
    mock_auth_request,
    auth_request_response,
    set_linnworks_session_config,
    session_token,
):
    assert session.LinnworksAPISession._authorise_session() == session_token


def test_linnworks_api_session_authorizes_when_used_as_a_session_manager(
    mock_auth_request,
    auth_request_response,
    set_linnworks_session_config,
    session_token,
):
    with session.LinnworksAPISession():
        last_request = mock_auth_request.request_history[0]
        assert last_request.url == session.LinnworksAPISession.AUTH_URL
        assert session.LinnworksAPISession.session_token == session_token


def test_set_login_method_sets_application_id(requests_mock, application_id):
    session.LinnworksAPISession.set_login(application_id=application_id)
    assert session.LinnworksAPISession.application_id == application_id


def test_set_login_method_sets_application_secret(requests_mock, application_secret):
    session.LinnworksAPISession.set_login(application_secret=application_secret)
    assert session.LinnworksAPISession.application_secret == application_secret


def test_set_login_method_sets_application_token(requests_mock, application_token):
    session.LinnworksAPISession.set_login(application_token=application_token)
    assert session.LinnworksAPISession.application_token == application_token


def test_find_config_filepath_returns_config_file_in_cwd(temp_cwd, config_file):
    path = session.LinnworksAPISession.find_config_filepath()
    assert path == temp_cwd / session.LinnworksAPISession.CONFIG_FILENAME


def test_find_config_filepath_returns_None_without_config_file_in_cwd():
    path = session.LinnworksAPISession.find_config_filepath()
    assert path is None


def test_load_from_config_file_sets_application_id(config_file, application_id):
    session.LinnworksAPISession.load_from_config_file(config_file)
    assert session.LinnworksAPISession.application_id == application_id


def test_load_from_config_file_sets_application_secret(config_file, application_secret):
    session.LinnworksAPISession.load_from_config_file(config_file)
    assert session.LinnworksAPISession.application_secret == application_secret


def test_load_from_config_file_sets_application_token(config_file, application_token):
    session.LinnworksAPISession.load_from_config_file(config_file)
    assert session.LinnworksAPISession.application_token == application_token


def test_enter_method_loads_credentials_from_file_if_not_set(
    mock_auth_request,
    config_file,
    application_id,
    application_secret,
    application_token,
):
    with session.LinnworksAPISession():
        pass
    assert session.LinnworksAPISession.application_id == application_id
    assert session.LinnworksAPISession.application_secret == application_secret
    assert session.LinnworksAPISession.application_token == application_token


def test_enter_method_does_not_load_credentials_if_already_set(
    mock_auth_request, config_file
):
    temp_value = "tmp_value"
    session.LinnworksAPISession.application_id = temp_value
    session.LinnworksAPISession.application_secret = temp_value
    session.LinnworksAPISession.application_token = temp_value
    with session.LinnworksAPISession():
        pass
    assert session.LinnworksAPISession.application_id == temp_value
    assert session.LinnworksAPISession.application_secret == temp_value
    assert session.LinnworksAPISession.application_token == temp_value


def test_linnworks_api_session_wrapper(
    mock_auth_request, set_linnworks_session_config, session_token
):
    @session.linnworks_api_session
    def wrapped_function():
        assert session.LinnworksAPISession.session_token == session_token

    wrapped_function()
