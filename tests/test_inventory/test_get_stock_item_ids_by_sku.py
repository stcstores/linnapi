from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory
from linnapi.requests.inventory import GetStockItemIDsBySKU


@pytest.fixture
def sku():
    return "E32-99X-8G2"


@pytest.fixture
def stock_item_id():
    return "965c4c47-227d-4b87-913f-0114dab13b61"


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
def response_data(sku, stock_item_id):
    return {
        "Items": [
            {
                "StockItemId": stock_item_id,
                "SKU": sku,
            }
        ]
    }


@pytest.fixture
def multiple_response_data(skus, stock_item_ids):
    return {
        "Items": [
            {
                "StockItemId": stock_item_id,
                "SKU": sku,
            }
            for sku, stock_item_id in zip(skus, stock_item_ids, strict=True)
        ]
    }


@pytest.fixture
def mock_single_response(response_data):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = response_data
        yield mock_make_request


@pytest.fixture
def mock_multiple_response(multiple_response_data):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response_data
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = {"invalid_key": "invalid_value"}
        yield mock_make_request


def test_get_stock_item_ids_by_sku_return_value(
    mock_single_response, sku, stock_item_id
):
    returned_value = inventory.get_stock_item_ids_by_sku([sku])
    assert returned_value == {sku: stock_item_id}


def test_get_stock_item_ids_by_sku_makes_request(mock_single_response, sku):
    inventory.get_stock_item_ids_by_sku([sku])
    mock_single_response.assert_called_once_with(GetStockItemIDsBySKU, skus=([sku],))


def test_get_stock_item_ids_by_sku_makes_request_with_multiple_skus(
    mock_multiple_response, skus
):
    inventory.get_stock_item_ids_by_sku(skus)
    mock_multiple_response.assert_called_once_with(GetStockItemIDsBySKU, skus=(skus,))


def test_get_stock_item_ids_by_sku_return_value_multiple_skus(
    mock_multiple_response, skus, stock_item_ids
):
    returned_value = inventory.get_stock_item_ids_by_sku([sku])
    assert returned_value == {
        sku: stock_item_id
        for sku, stock_item_id in zip(skus, stock_item_ids, strict=True)
    }


def test_get_stock_item_ids_by_sku_invalid_response(mock_invalid_response, sku):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_stock_item_ids_by_sku(sku)
