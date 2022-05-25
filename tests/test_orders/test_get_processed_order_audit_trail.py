from unittest.mock import patch

import pytest

from linnapi import exceptions, models, orders


@pytest.fixture
def order_guid():
    return "73846ae8-9f64-42ef-8d76-31aa418da9d5"


@pytest.fixture
def response_item():
    return {
        "sid_history": 53825,
        "fkOrderId": "73846ae8-9f64-42ef-8d76-31aa418da9d5",
        "HistoryNote": "Order line MAY-YVP-78Y sent to store",
        "fkOrderHistoryTypeId": "DESPATCH_NOTE",
        "DateStamp": "2022-05-23T07:27:54.903Z",
        "Tag": "CONFIRMED",
        "UpdatedBy": "SYNC",
        "TypeDescription": "Dispatch note has been sent to channel",
    }


@pytest.fixture
def single_response(response_item):
    return [response_item]


@pytest.fixture
def multiple_response(response_item):
    return [response_item, response_item, response_item]


@pytest.fixture
def mock_single_response(single_response):
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = single_response
        yield mock_make_request


@pytest.fixture
def mock_multiple_response(multiple_response):
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = {"invalid_key": "invalid_value"}
        yield mock_make_request


def test_get_inventory_item_images_makes_request(mock_single_response, order_guid):
    orders.get_processed_order_audit_trail(order_guid)
    mock_single_response.called_once_with(
        orders.GetProcessedAuditTrail, order_guid=order_guid
    )


def test_get_inventory_item_images_single_return_value(
    mock_single_response, order_guid
):
    returned_value = orders.get_processed_order_audit_trail(order_guid)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 1
    assert isinstance(returned_value[0], models.OrderAuditTrailEntry)


def test_get_inventory_item_images_single_multiple_value(
    mock_multiple_response, order_guid
):
    returned_value = orders.get_processed_order_audit_trail(order_guid)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 3
    assert all(
        (
            isinstance(value, models.OrderAuditTrailEntry) is True
            for value in returned_value
        )
    )


def test_get_inventory_item_images_with_invalid_response(
    mock_invalid_response, order_guid
):
    with pytest.raises(exceptions.InvalidResponseError):
        orders.get_processed_order_audit_trail(order_guid)
