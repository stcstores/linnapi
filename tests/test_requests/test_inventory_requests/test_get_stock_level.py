from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def stock_item_id():
    return "1649861651"


def test_get_stock_level_url():
    url = "https://eu-ext.linnworks.net/api/Stock/GetStockLevel"
    assert inventory.GetStockLevel.URL == url


def test_get_stock_level_method():
    assert inventory.GetStockLevel.METHOD == "POST"


def test_get_stock_level_headers(stock_item_id):
    assert inventory.GetStockLevel.headers(stock_item_id=stock_item_id) == {}


def test_get_stock_level_params(stock_item_id):
    assert inventory.GetStockLevel.params(stock_item_id=stock_item_id) is None


def test_get_stock_level_data(stock_item_id):
    assert inventory.GetStockLevel.data(stock_item_id=stock_item_id) is None


def test_get_stock_level_json(stock_item_id):
    expected_response = {"stockItemId": stock_item_id}
    assert (
        inventory.GetStockLevel.json(stock_item_id=stock_item_id) == expected_response
    )


def test_get_stock_level_parse_response(stock_item_id):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.GetStockLevel.parse_response(response, stock_item_id=stock_item_id)
        == response.json.return_value
    )
