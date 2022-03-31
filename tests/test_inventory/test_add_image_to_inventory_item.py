from unittest.mock import patch

import pytest

from linnapi import inventory
from linnapi.models import InventoryItemImage
from linnapi.requests.inventory import AddImageToInventoryItem


@pytest.fixture
def sku():
    return "E32-99X-8G2"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def image_url():
    return "http://test.com/image.jpg"


@pytest.fixture
def add_image_to_inventory_item_response():
    return {
        "StockItemId": "972af264-d768-4c6c-9152-0ad9d9d5b352",
        "ImageId": "eea21827-491d-4022-996a-d068dd6b25ea",
        "ImageUrl": "https://image.jpg",
        "ImageThumbnailUrl": "https://image_thumbanil.jpg",
    }


@pytest.fixture
def mock_make_request(add_image_to_inventory_item_response):
    with patch("linnapi.inventory.make_request") as mock_request:
        mock_request.return_value = add_image_to_inventory_item_response
        yield mock_request


def test_add_image_to_inventory_item_makes_request_with_sku(
    mock_make_request, sku, image_url
):
    inventory.add_image_to_inventory_item(sku=sku, image_url=image_url, is_main=True)
    mock_make_request.assert_called_once_with(
        AddImageToInventoryItem,
        item_number=sku,
        is_main=True,
        image_url=image_url,
        stock_item_id=None,
    )


def test_add_image_to_inventory_item_makes_request_with_stock_item_id(
    mock_make_request, stock_item_id, image_url
):
    inventory.add_image_to_inventory_item(
        stock_item_id=stock_item_id, image_url=image_url, is_main=True
    )
    mock_make_request.assert_called_once_with(
        AddImageToInventoryItem,
        item_number=None,
        is_main=True,
        image_url=image_url,
        stock_item_id=stock_item_id,
    )


def test_add_image_to_inventory_item_makes_request_without_is_main(
    mock_make_request, stock_item_id, image_url
):
    inventory.add_image_to_inventory_item(
        stock_item_id=stock_item_id, image_url=image_url
    )
    mock_make_request.assert_called_once_with(
        AddImageToInventoryItem,
        item_number=None,
        is_main=False,
        image_url=image_url,
        stock_item_id=stock_item_id,
    )


def test_add_image_to_inventory_item_makes_request_with_stock_item_id_and_sku(
    mock_make_request, stock_item_id, image_url, sku
):
    inventory.add_image_to_inventory_item(
        stock_item_id=stock_item_id, image_url=image_url, sku=sku, is_main=True
    )
    mock_make_request.assert_called_once_with(
        AddImageToInventoryItem,
        item_number=sku,
        is_main=True,
        image_url=image_url,
        stock_item_id=stock_item_id,
    )


def test_add_image_to_inventory_item_return_value(
    mock_make_request,
    sku,
    image_url,
    add_image_to_inventory_item_response,
):
    returned_value = inventory.add_image_to_inventory_item(
        sku=sku, image_url=image_url, is_main=True
    )
    assert type(returned_value) == InventoryItemImage
    assert returned_value.image_id == add_image_to_inventory_item_response["ImageId"]
