from unittest.mock import patch

import pytest

from linnapi import exceptions, orders


@pytest.fixture
def order_id():
    return "98743579"


@pytest.fixture
def order_guid():
    return "73846ae8-9f64-42ef-8d76-31aa418da9d5"


@pytest.fixture
def mock_response(order_guid):
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = {"OrderId": order_guid}
        yield mock_make_request


@pytest.fixture
def mock_failed_response(order_guid):
    with patch(
        "linnapi.orders.make_request", side_effect=Exception("Test")
    ) as mock_make_request:
        yield mock_make_request


def test_get_order_guid_by_order_id_returns_order_guid(
    mock_response, order_id, order_guid
):
    assert orders.get_order_guid_by_order_id(order_id) == order_guid


def test_get_order_guid_by_order_id_accepts_ints(mock_response, order_id, order_guid):
    assert orders.get_order_guid_by_order_id(int(order_id)) == order_guid


def test_get_order_guid_by_order_id_raises_when_order_id_key_not_present(
    mock_response, order_id
):
    mock_response.return_value = {}
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(order_id)
    assert str(excinfo.value) == "Response did not contain an order GUID."


def test_get_order_guid_by_order_id_raises_when_response_is_not_JSON(
    mock_response, order_id
):
    mock_response.return_value = "Error"
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(order_id)
    assert str(excinfo.value) == "Response did not contain an order GUID."


def test_get_order_guid_by_order_id_raises_when_request_fails(
    mock_failed_response, order_id, order_guid
):
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(order_id)
    assert str(excinfo.value) == f"Failed to retrieve order GUID for order {order_id}"
