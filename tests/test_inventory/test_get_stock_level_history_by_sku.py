from unittest.mock import patch

import pytest

from linnapi import inventory


@pytest.fixture
def sku():
    return "E32-99X-8G2"


@pytest.fixture
def location_id():
    return "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def stock_item_id():
    return "965c4c47-227d-4b87-913f-0114dab13b61"


@pytest.fixture
def mock_get_stock_item_id_by_sku(stock_item_id):
    with patch(
        "linnapi.inventory.get_stock_item_id_by_sku"
    ) as mock_get_stock_item_id_by_sku:
        mock_get_stock_item_id_by_sku.return_value = stock_item_id
        yield mock_get_stock_item_id_by_sku


@pytest.fixture
def mock_get_stock_level_history_by_stock_item_id(stock_item_id):
    with patch(
        "linnapi.inventory.get_stock_level_history_by_stock_item_id"
    ) as mock_get_stock_level_history_by_stock_item_id:
        yield mock_get_stock_level_history_by_stock_item_id


def test_get_stock_level_history_by_sku_calls_get_stock_item_id_by_sku(
    mock_get_stock_item_id_by_sku,
    mock_get_stock_level_history_by_stock_item_id,
    sku,
    location_id,
):
    inventory.get_stock_level_history_by_sku(sku=sku, location_id=location_id)
    mock_get_stock_item_id_by_sku.assert_called_once_with(sku)


def test_get_stock_level_history_by_sku_calls_get_stock_level_history_by_stock_item_id(
    mock_get_stock_item_id_by_sku,
    mock_get_stock_level_history_by_stock_item_id,
    stock_item_id,
    sku,
    location_id,
):
    inventory.get_stock_level_history_by_sku(sku=sku, location_id=location_id)
    mock_get_stock_level_history_by_stock_item_id.assert_called_once_with(
        stock_item_id=stock_item_id, location_id=location_id
    )


def test_get_stock_level_history_by_sku_calls_return_value(
    mock_get_stock_item_id_by_sku,
    mock_get_stock_level_history_by_stock_item_id,
    sku,
    location_id,
):
    returned_value = inventory.get_stock_level_history_by_sku(
        sku=sku, location_id=location_id
    )
    assert returned_value == mock_get_stock_level_history_by_stock_item_id.return_value
