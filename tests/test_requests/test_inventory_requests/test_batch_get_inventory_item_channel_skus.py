from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def stock_item_ids():
    return [
        "f81f4a9a-951e-4322-aba8-267ede814105",
        "fa2af046-4cd9-48e3-ad40-35dc9ec7e1f4",
    ]


def test_get_stock_item_ids_by_sku_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/BatchGetInventoryItemChannelSKUs"
    assert inventory.BatchGetInventoryItemChannelSKUs.URL == url


def test_get_stock_item_ids_by_sku_method():
    assert inventory.BatchGetInventoryItemChannelSKUs.METHOD == "POST"


def test_get_stock_item_ids_by_sku_headers(stock_item_ids):
    assert (
        inventory.BatchGetInventoryItemChannelSKUs.headers(
            stock_item_ids=stock_item_ids
        )
        == {}
    )


def test_get_stock_item_ids_by_sku_params(stock_item_ids):
    assert (
        inventory.BatchGetInventoryItemChannelSKUs.params(stock_item_ids=stock_item_ids)
        is None
    )


def test_get_stock_item_ids_by_sku_data(stock_item_ids):
    assert (
        inventory.BatchGetInventoryItemChannelSKUs.data(stock_item_ids=stock_item_ids)
        is None
    )


def test_get_stock_item_ids_by_sku_json(stock_item_ids):
    expected_response = {"inventoryItemIds": stock_item_ids}
    assert (
        inventory.BatchGetInventoryItemChannelSKUs.json(stock_item_ids=stock_item_ids)
        == expected_response
    )


def test_get_stock_item_ids_by_sku_parse_response(stock_item_ids):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.BatchGetInventoryItemChannelSKUs.parse_response(
            response, stock_item_ids=stock_item_ids
        )
        == response.json.return_value
    )
