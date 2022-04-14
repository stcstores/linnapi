from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory
from linnapi.models import StockLevelInfo
from linnapi.requests.inventory import GetStockLevel


@pytest.fixture
def stock_item_id():
    return "965c4c47-227d-4b87-913f-0114dab13b61"


@pytest.fixture
def get_stock_level_response(stock_item_id):
    return {
        "Location": {
            "StockLocationId": "00000000-0000-0000-0000-000000000000",
            "StockLocationIntId": 0,
            "LocationName": "Default",
            "IsFulfillmentCenter": False,
            "IsWarehouseManaged": False,
        },
        "StockLevel": 3,
        "StockValue": 0.0,
        "MinimumLevel": 4,
        "InOrderBook": 0,
        "Due": 0,
        "JIT": False,
        "InOrders": 0,
        "Available": 3,
        "UnitCost": 0.0,
        "SKU": "E32-99X-8G2",
        "AutoAdjust": True,
        "LastUpdateDate": "2022-03-15T14:31:09.103Z",
        "LastUpdateOperation": "DIRECT ADJUSTMENT BY stcadmin",
        "rowid": "2df49516-77f7-4eb6-aa75-dd6ae9ec7e82",
        "PendingUpdate": False,
        "StockItemPurchasePrice": 9.6,
        "StockItemId": stock_item_id,
        "StockItemIntId": 0,
    }


@pytest.fixture
def mock_make_request(get_stock_level_response):
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = [get_stock_level_response]
        yield mock_request


@pytest.fixture
def mock_make_request_with_invalid_response(get_stock_level_response):
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = [{"invalid_key": "invalid_value"}]
        yield mock_request


def test_get_stock_level_by_stock_id_return_value(
    mock_make_request, stock_item_id, get_stock_level_response
):
    returned_value = inventory.get_stock_level_by_stock_id(stock_item_id=stock_item_id)
    assert type(returned_value) == StockLevelInfo
    assert returned_value.stock_level == get_stock_level_response["StockLevel"]


def test_get_stock_level_by_stock_id_makes_request(mock_make_request, stock_item_id):
    inventory.get_stock_level_by_stock_id(stock_item_id=stock_item_id)
    mock_make_request.assert_called_once_with(
        GetStockLevel, stock_item_id=stock_item_id
    )


def test_invaild_response(mock_make_request_with_invalid_response, stock_item_id):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_stock_level_by_stock_id(stock_item_id=stock_item_id)
