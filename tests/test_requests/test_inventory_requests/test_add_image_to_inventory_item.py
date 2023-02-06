from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def item_number():
    return "aaa-bbb-ccc"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def image_url():
    return "http://test.com/image.jpg"


def test_add_image_to_inventory_item_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/AddImageToInventoryItem"
    assert inventory.AddImageToInventoryItem.URL == url


def test_add_image_to_inventory_item_method():
    assert inventory.AddImageToInventoryItem.METHOD == "POST"


def test_add_image_to_inventory_item_headers(item_number, image_url):
    assert (
        inventory.AddImageToInventoryItem.headers(
            item_number=item_number, image_url=image_url, is_main=True
        )
        == {}
    )


def test_add_image_to_inventory_item_params(item_number, image_url):
    assert (
        inventory.AddImageToInventoryItem.params(
            item_number=item_number, image_url=image_url, is_main=True
        )
        is None
    )


def test_add_image_to_inventory_item_data(item_number, image_url):
    assert (
        inventory.AddImageToInventoryItem.data(
            item_number=item_number, image_url=image_url, is_main=True
        )
        is None
    )


def test_add_image_to_inventory_item_json_with_item_number(item_number, image_url):
    expected_response = {
        "request": {"ItemNumber": item_number, "ImageUrl": image_url, "IsMain": True}
    }
    assert (
        inventory.AddImageToInventoryItem.json(
            item_number=item_number, image_url=image_url, is_main=True
        )
        == expected_response
    )


def test_add_image_to_inventory_item_json_with_stock_item_id(stock_item_id, image_url):
    expected_response = {
        "request": {"StockItemId": stock_item_id, "ImageUrl": image_url, "IsMain": True}
    }
    assert (
        inventory.AddImageToInventoryItem.json(
            stock_item_id=stock_item_id, image_url=image_url, is_main=True
        )
        == expected_response
    )


def test_add_image_to_inventory_item_json_with_item_number_and_stock_item_id(
    stock_item_id, item_number, image_url
):
    expected_response = {
        "request": {
            "StockItemId": stock_item_id,
            "ItemNumber": item_number,
            "ImageUrl": image_url,
            "IsMain": True,
        }
    }
    assert (
        inventory.AddImageToInventoryItem.json(
            stock_item_id=stock_item_id,
            item_number=item_number,
            image_url=image_url,
            is_main=True,
        )
        == expected_response
    )


def test_add_image_to_inventory_item_json_without_item_number_or_stock_item_id(
    image_url,
):
    with pytest.raises(ValueError):
        inventory.AddImageToInventoryItem.json(
            image_url=image_url,
            is_main=True,
        )


def test_add_image_to_inventory_item_parse_response(item_number, image_url):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        inventory.AddImageToInventoryItem.parse_response(
            response, item_number=item_number, image_url=image_url, is_main=True
        )
        == response.json.return_value
    )
