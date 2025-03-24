from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory, models
from linnapi.requests.inventory import GetItemChangesHistory


@pytest.fixture
def stock_item_id():
    return "1c419f0b-b066-4c8b-8970-be7c19b91614"


@pytest.fixture
def location_id():
    return "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def call_response():
    return {
        "PageNumber": 0,
        "EntriesPerPage": 0,
        "TotalEntries": 2,
        "TotalPages": 0,
        "Data": [
            {
                "Date": "2022-04-11T13:32:10.993Z",
                "Level": 44,
                "StockValue": 0.0,
                "Note": "Imported from file",
                "ChangeQty": 44,
                "ChangeValue": 0.0,
                "StockItemId": "6079faa4-e4ff-4b5b-9990-fc571e70412e",
                "StockItemIntId": 0,
            },
            {
                "Date": "2022-04-06T13:26:50.257Z",
                "Level": 0,
                "StockValue": 0.0,
                "Note": "Imported from file",
                "ChangeQty": 0,
                "ChangeValue": 0.0,
                "StockItemId": "6079faa4-e4ff-4b5b-9990-fc571e70412e",
                "StockItemIntId": 0,
            },
        ],
    }


@pytest.fixture
def call_response_out_of_order():
    return {
        "PageNumber": 0,
        "EntriesPerPage": 0,
        "TotalEntries": 2,
        "TotalPages": 0,
        "Data": [
            {
                "Date": "2022-04-06T13:26:50.257Z",
                "Level": 0,
                "StockValue": 0.0,
                "Note": "Imported from file",
                "ChangeQty": 0,
                "ChangeValue": 0.0,
                "StockItemId": "6079faa4-e4ff-4b5b-9990-fc571e70412e",
                "StockItemIntId": 0,
            },
            {
                "Date": "2022-04-11T13:32:10.993Z",
                "Level": 44,
                "StockValue": 0.0,
                "Note": "Imported from file",
                "ChangeQty": 44,
                "ChangeValue": 0.0,
                "StockItemId": "6079faa4-e4ff-4b5b-9990-fc571e70412e",
                "StockItemIntId": 0,
            },
        ],
    }


@pytest.fixture
def invalid_response():
    return {"key": "value"}


@pytest.fixture
def mock_make_request(
    call_response,
):
    with patch("linnapi.inventory.make_request") as mock_method:
        mock_method.return_value = call_response
        yield mock_method


def test_get_stock_level_history_by_stock_item_id_calls_make_request(
    mock_make_request, stock_item_id, location_id
):
    inventory.get_stock_level_history_by_stock_item_id(
        stock_item_id=stock_item_id,
        location_id=location_id,
        entries_per_page=50,
        page_number=3,
    )
    mock_make_request.assert_called_once_with(
        GetItemChangesHistory,
        stock_item_id=stock_item_id,
        location_id=location_id,
        entries_per_page=50,
        page_number=3,
    )


def test_get_stock_level_history_by_stock_item_id_calls_make_request_with_default_parameters(
    mock_make_request, stock_item_id, location_id
):
    inventory.get_stock_level_history_by_stock_item_id(
        stock_item_id=stock_item_id, location_id=location_id
    )
    mock_make_request.assert_called_once_with(
        GetItemChangesHistory,
        stock_item_id=stock_item_id,
        location_id=location_id,
        entries_per_page=500,
        page_number=1,
    )


def test_get_stock_level_history_by_stock_item_id_return_value(
    mock_make_request, call_response, stock_item_id, location_id
):
    returned_value = inventory.get_stock_level_history_by_stock_item_id(
        stock_item_id=stock_item_id, location_id=location_id
    )
    assert type(returned_value) is list
    assert len(returned_value) == len(call_response["Data"])
    for i, obj in enumerate(returned_value):
        assert type(obj) is models.StockItemHistoryRecord
        assert obj.stock_item_id == call_response["Data"][i]["StockItemId"]


def test_get_stock_level_history_by_stock_item_id_with_invalid_response(
    stock_item_id, location_id, invalid_response, mock_make_request
):
    mock_make_request.return_value = invalid_response
    with pytest.raises(exceptions.InvalidResponseError) as exc_info:
        inventory.get_stock_level_history_by_stock_item_id(
            stock_item_id=stock_item_id, location_id=location_id
        )
    assert str(exc_info.value) == f"Invalid Response: {invalid_response}"


def test_get_stock_level_history_by_stock_item_id_sorts_response(
    mock_make_request, call_response_out_of_order, stock_item_id, location_id
):
    mock_make_request.return_value = call_response_out_of_order
    returned_value = inventory.get_stock_level_history_by_stock_item_id(
        stock_item_id=stock_item_id, location_id=location_id
    )
    assert returned_value == sorted(
        returned_value, key=lambda x: x.timestamp, reverse=True
    )
