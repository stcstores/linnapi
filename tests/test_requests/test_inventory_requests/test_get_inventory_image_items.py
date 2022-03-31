from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def inventory_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


def test_get_inventory_item_images_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/GetInventoryItemImages"
    assert inventory.GetInventoryItemImages.URL == url


def test_get_inventory_item_images_method():
    assert inventory.GetInventoryItemImages.METHOD == "POST"


def test_get_inventory_item_images_headers(inventory_item_id):
    assert (
        inventory.GetInventoryItemImages.headers(inventory_item_id=inventory_item_id)
        == {}
    )


def test_get_inventory_item_images_params(inventory_item_id):
    assert (
        inventory.GetInventoryItemImages.params(inventory_item_id=inventory_item_id)
        is None
    )


def test_get_inventory_item_images_data(inventory_item_id):
    assert (
        inventory.GetInventoryItemImages.data(inventory_item_id=inventory_item_id)
        is None
    )


def test_get_inventory_item_images_json(inventory_item_id):
    expected_response = {"inventoryItemId": inventory_item_id}
    assert (
        inventory.GetInventoryItemImages.json(inventory_item_id=inventory_item_id)
        == expected_response
    )


def test_get_inventory_item_images_parse_response(inventory_item_id):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.GetInventoryItemImages.parse_response(
            response, inventory_item_id=inventory_item_id
        )
        == response.json.return_value
    )
