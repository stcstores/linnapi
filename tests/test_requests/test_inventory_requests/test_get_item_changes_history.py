from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def stock_item_id():
    return "1c419f0b-b066-4c8b-8970-be7c19b91614"


@pytest.fixture
def location_id():
    return "00000000-0000-0000-0000-000000000000"


def test_get_item_changes_history_url():
    url = "https://eu-ext.linnworks.net/api/Stock/GetItemChangesHistory"
    assert inventory.GetItemChangesHistory.URL == url


def test_get_item_changes_history_method():
    assert inventory.GetItemChangesHistory.METHOD == "POST"


def test_get_item_changes_history_headers(stock_item_id, location_id):
    assert (
        inventory.GetItemChangesHistory.headers(
            stock_item_id=stock_item_id, location_id=location_id
        )
        == {}
    )


def test_get_item_changes_history_params(stock_item_id, location_id):
    expected_response = {
        "stockItemId": stock_item_id,
        "locationId": location_id,
        "entriesPerPage": 500,
        "pageNumber": 1,
    }
    assert (
        inventory.GetItemChangesHistory.params(
            stock_item_id=stock_item_id, location_id=location_id
        )
        == expected_response
    )


def test_get_item_changes_history_params_with_entries_per_page(
    stock_item_id, location_id
):
    expected_response = {
        "stockItemId": stock_item_id,
        "locationId": location_id,
        "entriesPerPage": 50,
        "pageNumber": 1,
    }
    assert (
        inventory.GetItemChangesHistory.params(
            stock_item_id=stock_item_id,
            location_id=location_id,
            entries_per_page=50,
        )
        == expected_response
    )


def test_get_item_changes_history_params_with_page_number(stock_item_id, location_id):
    expected_response = {
        "stockItemId": stock_item_id,
        "locationId": location_id,
        "entriesPerPage": 500,
        "pageNumber": 5,
    }
    assert (
        inventory.GetItemChangesHistory.params(
            stock_item_id=stock_item_id,
            location_id=location_id,
            page_number=5,
        )
        == expected_response
    )


def test_get_item_changes_history_data(stock_item_id, location_id):
    assert (
        inventory.GetItemChangesHistory.data(
            stock_item_id=stock_item_id, location_id=location_id
        )
        is None
    )


def test_get_item_changes_history_json(stock_item_id, location_id):
    assert (
        inventory.GetItemChangesHistory.json(
            stock_item_id=stock_item_id, location_id=location_id
        )
        is None
    )


def test_get_item_changes_history_parse_response(stock_item_id, location_id):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.GetItemChangesHistory.parse_response(
            response, stock_item_id=stock_item_id, location_id=location_id
        )
        == response.json.return_value
    )
