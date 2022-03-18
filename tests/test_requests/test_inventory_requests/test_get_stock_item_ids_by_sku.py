from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def skus():
    return ["aaa", "bbb"]


def test_get_stock_item_ids_by_sku_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/GetStockItemIdsBySKU"
    assert inventory.GetStockItemIDsBySKU.URL == url


def test_get_stock_item_ids_by_sku_method():
    assert inventory.GetStockItemIDsBySKU.METHOD == "POST"


def test_get_stock_item_ids_by_sku_headers(skus):
    assert inventory.GetStockItemIDsBySKU.headers(skus=skus) == {}


def test_get_stock_item_ids_by_sku_params(skus):
    assert inventory.GetStockItemIDsBySKU.params(skus=skus) is None


def test_get_stock_item_ids_by_sku_data(skus):
    assert inventory.GetStockItemIDsBySKU.data(skus=skus) is None


def test_get_stock_item_ids_by_sku_json(skus):
    expected_response = {"request": {"SKUS": skus}}
    assert inventory.GetStockItemIDsBySKU.json(skus=skus) == expected_response


def test_get_stock_item_ids_by_sku_parse_response(skus):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.GetStockItemIDsBySKU.parse_response(response, skus=skus)
        == response.json.return_value
    )
