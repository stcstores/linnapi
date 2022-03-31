from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def image_url():
    return "http://test.com/image.jpg"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def kwargs(image_url, stock_item_id):
    return {"image_url": image_url, "stock_item_id": stock_item_id}


def test_delete_images_from_inventory_item_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/DeleteImagesFromInventoryItem"
    assert inventory.DeleteImagesFromInventoryItem.URL == url


def test_delete_images_from_inventory_item_method():
    assert inventory.DeleteImagesFromInventoryItem.METHOD == "POST"


def test_delete_images_from_inventory_item_multi_headers(kwargs):
    assert inventory.DeleteImagesFromInventoryItem.headers([kwargs]) == {}


def test_delete_images_from_inventory_item_multi_params(kwargs):
    assert inventory.DeleteImagesFromInventoryItem.params([kwargs]) is None


def test_delete_images_from_inventory_item_multi_data(kwargs):
    assert inventory.DeleteImagesFromInventoryItem.multi_data([kwargs]) is None


def test_delete_images_from_inventory_item_multi_json(kwargs, stock_item_id, image_url):
    expected_response = {"inventoryItemImages": {stock_item_id: [image_url]}}
    assert (
        inventory.DeleteImagesFromInventoryItem.multi_json([kwargs])
        == expected_response
    )


def test_delete_images_from_inventory_item_multi_json_with_multiple_requests(
    kwargs, stock_item_id, image_url
):
    expected_response = {
        "inventoryItemImages": {
            "0001": [
                "https:test.com/image_1.jpg",
                "https:test.com/image_2.jpg",
                "https:test.com/image_3.jpg",
            ],
            "0002": [
                "https:test.com/image_4.jpg",
                "https:test.com/image_5.jpg",
                "https:test.com/image_6.jpg",
            ],
            "0003": ["https:test.com/image_7.jpg"],
        }
    }
    assert (
        inventory.DeleteImagesFromInventoryItem.multi_json(
            [
                {"stock_item_id": "0001", "image_url": "https:test.com/image_1.jpg"},
                {"stock_item_id": "0001", "image_url": "https:test.com/image_2.jpg"},
                {"stock_item_id": "0001", "image_url": "https:test.com/image_3.jpg"},
                {"stock_item_id": "0002", "image_url": "https:test.com/image_4.jpg"},
                {"stock_item_id": "0002", "image_url": "https:test.com/image_5.jpg"},
                {"stock_item_id": "0002", "image_url": "https:test.com/image_6.jpg"},
                {"stock_item_id": "0003", "image_url": "https:test.com/image_7.jpg"},
            ]
        )
        == expected_response
    )


def test_delete_images_from_inventory_item_multi_parse_response(kwargs):
    response = Mock()
    response.text = "Test Text"
    assert (
        inventory.DeleteImagesFromInventoryItem.parse_response(response, [kwargs])
        == response.text
    )
