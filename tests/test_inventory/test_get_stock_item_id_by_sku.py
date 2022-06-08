from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory


@pytest.fixture
def skus():
    return ["aaa", "bbb", "ccc"]


@pytest.fixture
def stock_item_ids():
    return [
        "d28efd06-57c4-4792-9048-50c31264acd3",
        "69a73aa0-f504-4f9a-ae59-13f6aae38279",
        "4a692c35-ef6c-4fde-9387-69a52625c7e6",
    ]


@pytest.fixture
def sku(skus):
    return skus[0]


@pytest.fixture
def stock_item_id(stock_item_ids):
    return stock_item_ids[0]


@pytest.fixture
def get_stock_item_ids_return_value(skus, stock_item_ids):
    return {sku: stock_item_id for sku, stock_item_id in zip(skus, stock_item_ids)}


@pytest.fixture
def mock_get_stock_item_ids(get_stock_item_ids_return_value):
    with patch("linnapi.inventory.get_stock_item_ids_by_sku") as mock_method:
        mock_method.return_value = get_stock_item_ids_return_value
        yield mock_method


def test_get_stock_item_id_by_sku_return_value(
    mock_get_stock_item_ids, sku, stock_item_id
):
    assert inventory.get_stock_item_id_by_sku(sku) == stock_item_id


def test_get_stock_item_id_by_sku_calls_get_stock_item_id_by_sku(
    mock_get_stock_item_ids, sku, stock_item_id
):
    inventory.get_stock_item_id_by_sku(sku)
    mock_get_stock_item_ids.assert_called_once_with(sku)


def test_get_stock_item_id_by_sku_with_invalid_response(mock_get_stock_item_ids):
    with pytest.raises(exceptions.InvalidResponseError) as exc_info:
        inventory.get_stock_item_id_by_sku("654166456")
        assert str(exc_info.value) == "Requested SKU not in response."
