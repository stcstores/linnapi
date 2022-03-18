from unittest.mock import patch

import pytest

from linnapi import inventory
from linnapi.models import StockLevelInfo
from linnapi.requests.inventory import SetStockLevelBySKU


@pytest.fixture
def sku():
    return "E32-99X-8G2"


@pytest.fixture
def location_id():
    "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def change_source():
    return "Change Source Text"


@pytest.fixture
def changes(sku):
    return [(sku, 3)]


@pytest.fixture
def set_stock_level_response(sku, location_id):
    return {
        "Location": {
            "StockLocationId": location_id,
            "StockLocationIntId": 0,
            "LocationName": "Default",
            "IsFulfillmentCenter": False,
        },
        "StockLevel": 0,
        "StockValue": 0.0,
        "MinimumLevel": 4,
        "InOrderBook": 0,
        "Due": 0,
        "JIT": False,
        "InOrders": 0,
        "Available": 0,
        "UnitCost": 9.6,
        "SKU": sku,
        "AutoAdjust": True,
        "LastUpdateDate": "2022-03-18T15:22:06.273Z",
        "LastUpdateOperation": "DIRECT ADJUSTMENT BY stcadmin",
        "rowid": "2df49516-77f7-4eb6-aa75-dd6ae9ec7e82",
        "PendingUpdate": False,
        "StockItemPurchasePrice": 9.6,
        "StockItemId": "965c4c47-227d-4b87-913f-0114dab13b61",
        "StockItemIntId": 0,
    }


@pytest.fixture
def mock_make_request(set_stock_level_response):
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = [set_stock_level_response]
        yield mock_request


def test_set_stock_level_makes_request(
    mock_make_request, sku, location_id, change_source, changes
):
    inventory.set_stock_level(
        changes=changes, location_id=location_id, change_source=change_source
    )
    mock_make_request.assert_called_once_with(
        SetStockLevelBySKU,
        location_id=location_id,
        changes=changes,
        change_source=change_source,
    )


def test_set_stock_level_return_value(
    mock_make_request,
    sku,
    location_id,
    change_source,
    changes,
    set_stock_level_response,
):
    returned_value = inventory.set_stock_level(
        changes=changes, location_id=location_id, change_source=change_source
    )
    assert type(returned_value) == list
    assert len(returned_value) == 1
    assert type(returned_value[0]) == StockLevelInfo
    assert returned_value[0].stock_level == set_stock_level_response["StockLevel"]
