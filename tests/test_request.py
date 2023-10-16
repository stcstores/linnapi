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

multi_headers_values = {"header_key": "header_value"}
multi_params_values = [{"params_key": "params_value"}]
multi_data_values = [{"data_key": "data_value"}]
multi_json_values = [{"json_key": "json_value"}]


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
    assert (
        request.LinnworksAPIRequest.parse_response(mock_response) == mock_response_value
    )
    mock_response.json.assert_called_once_with()


def test_linnworks_api_request_multi_headers_method():
    assert request.LinnworksAPIRequest.multi_headers([{}]) == {}


def test_linnworks_api_request_multi_params_method():
    assert request.LinnworksAPIRequest.multi_params([{}]) is None


def test_linnworks_api_request_multi_data_method():
    assert request.LinnworksAPIRequest.multi_data([{}]) is None


def test_linnworks_api_request_multi_json_method():
    assert request.LinnworksAPIRequest.multi_json([{}]) is None


def test_linnworks_api_request_multi_parse_response_method(
    mock_response, mock_response_value
):
    assert (
        request.LinnworksAPIRequest.multi_parse_response(mock_response, [{}])
        == mock_response_value
    )
    mock_response.json.assert_called_once_with()


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
    mock_linnworks_session.session.request.assert_called_once_with(
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


def test_linnworks_api_request_subclass_multi_headers_method():
    assert TestLinnworksAPIRequest.multi_headers([{}]) == headers_values


def test_linnworks_api_request_subclass_multi_params_method():
    assert TestLinnworksAPIRequest.multi_params([{}]) == params_values


def test_linnworks_api_request_subclass_multi_data_method():
    assert TestLinnworksAPIRequest.multi_data([{}]) == data_values


def test_linnworks_api_request_subclass_multi_json_method():
    assert TestLinnworksAPIRequest.multi_json([{}]) == json_values


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
    mocked_request.headers.assert_called_once_with(1, 2, test_param=3)


def test_make_request_updates_headers_with_auth_token(
    mock_linnworks_session, mocked_request
):
    args, kwargs = mock_linnworks_session.session.request.call_args
    assert kwargs["headers"] == mock_linnworks_session.request_headers.return_value


def test_make_request_calls_params(mocked_request):
    mocked_request.params.assert_called_once_with(1, 2, test_param=3)


def test_make_request_calls_data(mocked_request):
    mocked_request.data.assert_called_once_with(1, 2, test_param=3)


def test_make_request_calls_json(mocked_request):
    mocked_request.json.assert_called_once_with(1, 2, test_param=3)


def test_make_request_calls_parse_response(mocked_request, mock_response):
    mocked_request.parse_response.assert_called_once_with(
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


def test_multi_item_request_has_requests():
    assert request.MultiItemRequest().requests == []


def test_multi_item_request__add_request_method():
    requester = request.MultiItemRequest()
    request_params = {"key", "value"}
    requester._add_request(request_params)
    assert requester.requests == [request_params]


def test_multi_item_request_base_class_add_request_method_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        request.MultiItemRequest().add_request({})


class TestLinnworksAPIRequestMultiple(request.LinnworksAPIRequest):
    @classmethod
    def multi_headers(cls, requests):
        return multi_headers_values

    @classmethod
    def multi_params(cls, requests):
        return multi_params_values

    @classmethod
    def multi_data(cls, requests):
        return multi_data_values

    @classmethod
    def multi_json(cls, requests):
        return multi_json_values


class MultiItemRequestSubclassTest(request.MultiItemRequest):
    request_method = TestLinnworksAPIRequestMultiple

    def add_request(self, key):
        self._add_request({"key": key})


@pytest.fixture
def multi_item_requester_with_request():
    requester = MultiItemRequestSubclassTest()
    requester.add_request(key="value")
    return requester


def test_multi_item_request_request_method_returns_request_json(
    mock_linnworks_session, multi_item_requester_with_request, mock_response_value
):
    assert multi_item_requester_with_request.request() == mock_response_value


def test_multi_item_request_request_method_makes_request(
    mock_linnworks_session, request_headers, multi_item_requester_with_request
):
    multi_item_requester_with_request.request()
    mock_linnworks_session.session.request.assert_called_once_with(
        url=request.LinnworksAPIRequest.URL,
        method=request.LinnworksAPIRequest.METHOD,
        headers=request_headers | multi_headers_values,
        params=multi_params_values,
        data=multi_data_values,
        json=multi_json_values,
    )
