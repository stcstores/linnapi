from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def location_id():
    return "aaa-bbb-ccc"


@pytest.fixture
def change_source():
    return "Change Source Text"


@pytest.fixture
def changes():
    return [("aaa", 5), ("bbb", -3)]


def test_set_stock_level_by_sku_url():
    url = "https://eu-ext.linnworks.net/api/Stock/UpdateStockLevelsBySKU"
    assert inventory.SetStockLevelBySKU.URL == url


def test_set_stock_level_by_sku_method():
    assert inventory.SetStockLevelBySKU.METHOD == "POST"


def test_set_stock_level_by_sku_headers(location_id, changes, change_source):
    assert (
        inventory.SetStockLevelBySKU.headers(
            location_id=location_id, changes=changes, change_source=change_source
        )
        == {}
    )


def test_set_stock_level_by_sku_params(location_id, changes, change_source):
    assert inventory.SetStockLevelBySKU.params(
        location_id=location_id, changes=changes, change_source=change_source
    ) == {"changeSource": change_source}


def test_set_stock_level_by_sku_data(location_id, changes, change_source):
    assert (
        inventory.SetStockLevelBySKU.data(
            location_id=location_id, changes=changes, change_source=change_source
        )
        is None
    )


def test_set_stock_level_by_sku_json(location_id, changes, change_source):
    expected_response = {
        "stockLevels": [
            {"SKU": "aaa", "LocationID": location_id, "Level": 5},
            {"SKU": "bbb", "LocationID": location_id, "Level": -3},
        ]
    }
    assert (
        inventory.SetStockLevelBySKU.json(
            location_id=location_id, changes=changes, change_source=change_source
        )
        == expected_response
    )


def test_set_stock_level_by_sku_parse_response(location_id, changes, change_source):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.SetStockLevelBySKU.parse_response(
            response,
            location_id=location_id,
            changes=changes,
            change_source=change_source,
        )
        == response.json.return_value
    )
