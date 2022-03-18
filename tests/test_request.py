from unittest.mock import Mock, patch

import pytest

from linnapi import request


@pytest.fixture
def mock_response_value():
    return {"key": "value"}


@pytest.fixture
def request_headers():
    return {"Authorization": "mock_token"}


@pytest.fixture
def mock_response(mock_response_value):
    mock_request_response = Mock()
    mock_request_response.json.return_value = mock_response_value
    return mock_request_response


@pytest.fixture
def mock_linnworks_session(mock_response, request_headers):
    with patch("linnapi.request.LinnworksAPISession") as mock_linnworks_session:
        mock_linnworks_session.session.request.return_value = mock_response
        mock_linnworks_session.request_headers.return_value = request_headers
        yield mock_linnworks_session


headers_values = {"header_key": "header_value"}
params_values = {"params_key": "params_value"}
data_values = {"data_key": "data_value"}
json_values = {"json_key": "json_value"}


def test_linnworks_api_request_headers_method():
    assert request.LinnworksAPIRequest.headers() == {}


def test_linnworks_api_request_params_method():
    assert request.LinnworksAPIRequest.params() is None


def test_linnworks_api_request_data_method():
    assert request.LinnworksAPIRequest.data() is None


def test_linnworks_api_request_json_method():
    assert request.LinnworksAPIRequest.json() is None


def test_linnworks_api_request_parse_response_method(
    mock_response, mock_response_value
):
    assert mock_response.json.called_once_with()
    assert (
        request.LinnworksAPIRequest.parse_response(mock_response) == mock_response_value
    )


class TestLinnworksAPIRequest(request.LinnworksAPIRequest):
    @classmethod
    def headers(cls, *args, **kwargs):
        return headers_values

    @classmethod
    def params(cls, *args, **kwargs):
        return params_values

    @classmethod
    def data(cls, *args, **kwargs):
        return data_values

    @classmethod
    def json(cls, *args, **kwargs):
        return json_values


def test_make_request_returns_request_json(mock_linnworks_session, mock_response_value):
    assert request.make_request(request.LinnworksAPIRequest) == mock_response_value


def test_make_request_makes_request(
    mock_linnworks_session, request_headers, mock_response_value
):
    request.make_request(request.LinnworksAPIRequest)
    assert mock_linnworks_session.session.request.called_once_with(
        url=request.LinnworksAPIRequest.URL,
        method=request.LinnworksAPIRequest.METHOD,
        headers=request_headers,
        params=None,
        data=None,
        json=None,
    )


def test_linnworks_api_request_subclass_headers_method():
    assert TestLinnworksAPIRequest.headers() == headers_values


def test_linnworks_api_request_subclass_params_method():
    assert TestLinnworksAPIRequest.params() == params_values


def test_linnworks_api_request_subclass_data_method():
    assert TestLinnworksAPIRequest.data() == data_values


def test_linnworks_api_request_subclass_json_method():
    assert TestLinnworksAPIRequest.json() == json_values


@pytest.fixture
def mocked_request(mock_linnworks_session):
    request_class = Mock()
    request_class.headers.return_value = {}
    request.make_request(request_class, 1, 2, test_param=3)
    return request_class


@pytest.fixture
def request_with_test_request_subclass(mock_linnworks_session):
    request.make_request(TestLinnworksAPIRequest)


@pytest.fixture()
def request_subclass_request_call(
    mock_linnworks_session, request_with_test_request_subclass
):
    _, kwargs = mock_linnworks_session.session.request.call_args
    return kwargs


def test_make_request_calls_headers(mocked_request):
    assert mocked_request.headers.called_once_with(1, 2, test_param=3)


def test_make_request_updates_headers_with_auth_token(
    mock_linnworks_session, mocked_request
):
    args, kwargs = mock_linnworks_session.session.request.call_args
    assert kwargs["headers"] == mock_linnworks_session.request_headers.return_value


def test_make_request_calls_params(mocked_request):
    assert mocked_request.params.called_once_with(1, 2, test_param=3)


def test_make_request_calls_data(mocked_request):
    assert mocked_request.data.called_once_with(1, 2, test_param=3)


def test_make_request_calls_json(mocked_request):
    assert mocked_request.json.called_once_with(1, 2, test_param=3)


def test_make_request_calls_parse_response(mocked_request, mock_response):
    assert mocked_request.parse_response.called_once_with(
        mock_response, 1, 2, test_param=3
    )


def test_make_request_uses_values_from_request_class_for_headers(
    mock_linnworks_session, request_subclass_request_call
):
    expected_headers = mock_linnworks_session.request_headers() | headers_values
    assert request_subclass_request_call["headers"] == expected_headers


def test_make_request_uses_values_from_request_class_for_params(
    request_subclass_request_call,
):
    assert request_subclass_request_call["params"] == params_values


def test_make_request_uses_values_from_request_class_for_data(
    request_subclass_request_call,
):
    assert request_subclass_request_call["data"] == data_values


def test_make_request_uses_values_from_request_class_for_json(
    request_subclass_request_call,
):
    assert request_subclass_request_call["json"] == json_values
