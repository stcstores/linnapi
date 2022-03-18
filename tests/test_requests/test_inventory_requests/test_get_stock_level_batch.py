from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def stock_item_ids():
    return ["aaa", "bbb"]


def test_get_stock_level_batch_url():
    url = "https://eu-ext.linnworks.net/api/Stock/GetStockLevel_Batch"
    assert inventory.GetStockLevelBatch.URL == url


def test_get_stock_level_batch_method():
    assert inventory.GetStockLevelBatch.METHOD == "POST"


def test_get_stock_level_batch_headers(stock_item_ids):
    assert inventory.GetStockLevelBatch.headers(stock_item_ids=stock_item_ids) == {}


def test_get_stock_level_batch_params(stock_item_ids):
    assert inventory.GetStockLevelBatch.params(stock_item_ids=stock_item_ids) is None


def test_get_stock_level_batch_data(stock_item_ids):
    assert inventory.GetStockLevelBatch.data(stock_item_ids=stock_item_ids) is None


def test_get_stock_level_batch_json(stock_item_ids):
    expected_response = {"request": {"StockItemIDs": stock_item_ids}}
    assert (
        inventory.GetStockLevelBatch.json(stock_item_ids=stock_item_ids)
        == expected_response
    )


def test_get_stock_level_batch_parse_response(stock_item_ids):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.GetStockLevelBatch.parse_response(
            response, stock_item_ids=stock_item_ids
        )
        == response.json.return_value
    )
