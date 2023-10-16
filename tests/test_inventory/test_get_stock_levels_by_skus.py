from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory
from linnapi.models import StockLevelInfo
from linnapi.requests.inventory import GetStockLevelBatch


@pytest.fixture
def stock_item_ids():
    return (
        "230b4a8d-c9ff-49a3-83cb-0762a382bc83",
        "bb1c56b4-38cf-476e-8ab8-0c000c1fb0bc",
        "0a58e73c-4c63-4849-83ff-2568cc64bb20",
    )


@pytest.fixture
def skus():
    return ("1G2-E6W-4RF", "MTN-EUM-75H", "868-HHW-8AK")


@pytest.fixture
def get_stock_level_batch_response(skus, stock_item_ids):
    return [
        {
            "pkStockItemId": "230b4a8d-c9ff-49a3-83cb-0762a382bc83",
            "StockItemLevels": [
                {
                    "Location": {
                        "StockLocationId": "00000000-0000-0000-0000-000000000000",
                        "StockLocationIntId": 0,
                        "LocationName": "Default",
                        "IsFulfillmentCenter": False,
                        "BinRack": "T-075",
                    },
                    "StockLevel": 7,
                    "StockValue": 0.0,
                    "MinimumLevel": 4,
                    "InOrderBook": 0,
                    "Due": 0,
                    "JIT": False,
                    "InOrders": 0,
                    "Available": 7,
                    "UnitCost": 0.0,
                    "SKU": "1G2-E6W-4RF",
                    "LastUpdateDate": "2022-04-11T13:32:10.917Z",
                    "rowid": "a7a86750-235f-4a25-9f68-2ef02f41f4c7",
                    "PendingUpdate": False,
                    "StockItemPurchasePrice": 2.0,
                    "StockItemId": "230b4a8d-c9ff-49a3-83cb-0762a382bc83",
                    "StockItemIntId": 0,
                }
            ],
        },
        {
            "pkStockItemId": "bb1c56b4-38cf-476e-8ab8-0c000c1fb0bc",
            "StockItemLevels": [
                {
                    "Location": {
                        "StockLocationId": "00000000-0000-0000-0000-000000000000",
                        "StockLocationIntId": 0,
                        "LocationName": "Default",
                        "IsFulfillmentCenter": False,
                        "BinRack": "E-214",
                    },
                    "StockLevel": 1,
                    "StockValue": 0.0,
                    "MinimumLevel": 4,
                    "InOrderBook": 0,
                    "Due": 0,
                    "JIT": False,
                    "InOrders": 0,
                    "Available": 1,
                    "UnitCost": 0.0,
                    "SKU": "MTN-EUM-75H",
                    "LastUpdateDate": "2022-04-11T13:32:10.917Z",
                    "rowid": "045b37b4-4aca-4afb-af67-f80b8b596a9a",
                    "PendingUpdate": False,
                    "StockItemPurchasePrice": 2.95,
                    "StockItemId": "bb1c56b4-38cf-476e-8ab8-0c000c1fb0bc",
                    "StockItemIntId": 0,
                }
            ],
        },
        {
            "pkStockItemId": "0a58e73c-4c63-4849-83ff-2568cc64bb20",
            "StockItemLevels": [
                {
                    "Location": {
                        "StockLocationId": "00000000-0000-0000-0000-000000000000",
                        "StockLocationIntId": 0,
                        "LocationName": "Default",
                        "IsFulfillmentCenter": False,
                        "BinRack": "E-095",
                    },
                    "StockLevel": 28,
                    "StockValue": 0.0,
                    "MinimumLevel": 4,
                    "InOrderBook": 0,
                    "Due": 0,
                    "JIT": False,
                    "InOrders": 0,
                    "Available": 28,
                    "UnitCost": 0.0,
                    "SKU": "868-HHW-8AK",
                    "LastUpdateDate": "2022-04-11T13:32:10.917Z",
                    "rowid": "1b411f48-7a62-4b3c-ad1e-d1834cdcd841",
                    "PendingUpdate": False,
                    "StockItemPurchasePrice": 2.0,
                    "StockItemId": "0a58e73c-4c63-4849-83ff-2568cc64bb20",
                    "StockItemIntId": 0,
                }
            ],
        },
    ]


@pytest.fixture
def mock_make_request(get_stock_level_batch_response):
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = get_stock_level_batch_response
        yield mock_request


@pytest.fixture
def mock_make_request_with_invalid_response():
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = [{"invalid_key": "invalid_value"}]
        yield mock_request


@pytest.fixture
def mock_make_request_with_empty_response():
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = []
        yield mock_request


@pytest.fixture
def mock_make_request_with_incorrect_product_in_response(
    get_stock_level_batch_response,
):
    with patch("linnapi.inventory.make_request") as mock_request:
        get_stock_level_batch_response[2]["StockItemLevels"][0]["SKU"] = "KIJ-GNA-5MP"
        mock_request.return_value = [get_stock_level_batch_response]
        yield mock_request


@pytest.fixture
def mock_get_stock_item_ids_by_sku(skus, stock_item_ids):
    with patch(
        "linnapi.inventory.get_stock_item_ids_by_sku"
    ) as mock_get_stock_item_ids_by_sku:
        return_value = {
            sku: stock_item_id for sku, stock_item_id in zip(skus, stock_item_ids)
        }
        mock_get_stock_item_ids_by_sku.return_value = return_value
        yield mock_get_stock_item_ids_by_sku


def test_get_stock_levels_by_skus_requests_stock_id(
    mock_get_stock_item_ids_by_sku, mock_make_request, skus
):
    inventory.get_stock_levels_by_skus(*skus)
    mock_get_stock_item_ids_by_sku.assert_called_once_with(*skus)


def test_get_stock_levels_by_skus_return_value(
    mock_get_stock_item_ids_by_sku,
    mock_make_request,
    stock_item_ids,
    skus,
    get_stock_level_batch_response,
):
    returned_value = inventory.get_stock_levels_by_skus(*skus)
    assert isinstance(returned_value, dict)
    assert len(returned_value) == 3
    for key, value in returned_value.items():
        assert isinstance(key, str)
        assert isinstance(value, StockLevelInfo)
    for i, sku in enumerate(skus):
        assert (
            returned_value[sku].stock_level
            == get_stock_level_batch_response[i]["StockItemLevels"][0]["StockLevel"]
        )


def test_get_stock_levels_by_skus_makes_request(
    mock_get_stock_item_ids_by_sku, mock_make_request, stock_item_ids, skus
):
    inventory.get_stock_levels_by_skus(*skus)
    mock_make_request.assert_called_once_with(
        GetStockLevelBatch, stock_item_ids=list(stock_item_ids)
    )


def test_invalid_response(
    mock_get_stock_item_ids_by_sku, mock_make_request_with_invalid_response, skus
):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_stock_levels_by_skus(*skus)


def test_empty_response(
    mock_get_stock_item_ids_by_sku, mock_make_request_with_empty_response, skus
):
    with pytest.raises(exceptions.IncompleteResponseError):
        inventory.get_stock_levels_by_skus(*skus)


def test_incorrect_product_in_response(
    mock_get_stock_item_ids_by_sku,
    mock_make_request_with_incorrect_product_in_response,
    skus,
):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_stock_levels_by_skus(*skus)
