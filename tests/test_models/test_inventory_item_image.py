import pytest

from linnapi import models


@pytest.fixture
def add_image_to_inventory_item_response():
    return {
        "StockItemId": "972af264-d768-4c6c-9152-0ad9d9d5b352",
        "ImageId": "eea21827-491d-4022-996a-d068dd6b25ea",
        "ImageUrl": "https://image.jpg",
        "ImageThumbnailUrl": "https://image_thumbanil.jpg",
    }


@pytest.fixture
def inventory_item_image_with_response(add_image_to_inventory_item_response):
    return models.InventoryItemImage(add_image_to_inventory_item_response)


def test_inventory_item_image_sets_raw(
    inventory_item_image_with_response, add_image_to_inventory_item_response
):
    assert (
        inventory_item_image_with_response.raw == add_image_to_inventory_item_response
    )


def test_inventory_item_image_sets_stock_item_id(
    inventory_item_image_with_response, add_image_to_inventory_item_response
):
    assert (
        inventory_item_image_with_response.stock_item_id
        == add_image_to_inventory_item_response["StockItemId"]
    )


def test_inventory_item_image_sets_image_id(
    inventory_item_image_with_response, add_image_to_inventory_item_response
):
    assert (
        inventory_item_image_with_response.image_id
        == add_image_to_inventory_item_response["ImageId"]
    )


def test_inventory_item_image_sets_image_url(
    inventory_item_image_with_response, add_image_to_inventory_item_response
):
    assert (
        inventory_item_image_with_response.image_url
        == add_image_to_inventory_item_response["ImageUrl"]
    )


def test_inventory_item_image_sets_in_order_image_thumbnail_url(
    inventory_item_image_with_response, add_image_to_inventory_item_response
):
    assert (
        inventory_item_image_with_response.image_thumbnail_url
        == add_image_to_inventory_item_response["ImageThumbnailUrl"]
    )
