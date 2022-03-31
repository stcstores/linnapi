import pytest

from linnapi import models


@pytest.fixture
def get_inventory_item_images_response():
    return {
        "Source": "https://test.com/d068dd6b25ea.jpg",
        "FullSource": "https://test.com/d068dd6b25ea.jpg",
        "CheckSumValue": "E2B590D292101E5C3801DAF3A187ACBBF9B628E19FE0108A357B7DD0639FFE54",
        "pkRowId": "eea21827-491d-4022-996a-d068dd6b25ea",
        "IsMain": True,
        "SortOrder": 0,
        "StockItemId": "972af264-d768-4c6c-9152-0ad9d9d5b352",
        "StockItemIntId": 0,
    }


@pytest.fixture
def stock_item_image_with_response(get_inventory_item_images_response):
    return models.StockItemImage(get_inventory_item_images_response)


def test_stock_item__image_sets_raw(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert stock_item_image_with_response.raw == get_inventory_item_images_response


def test_stock_item__image_sets_stock_item_id(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.stock_item_id
        == get_inventory_item_images_response["StockItemId"]
    )


def test_stock_item__image_sets_stock_item_int_id(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.stock_item_int_id
        == get_inventory_item_images_response["StockItemIntId"]
    )


def test_stock_item__image_sets_image_id(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.image_id
        == get_inventory_item_images_response["pkRowId"]
    )


def test_stock_item__image_sets_source(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.source
        == get_inventory_item_images_response["Source"]
    )


def test_stock_item__image_sets_full_source(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.full_source
        == get_inventory_item_images_response["FullSource"]
    )


def test_stock_item__image_sets_checksum_value(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.checksum_value
        == get_inventory_item_images_response["CheckSumValue"]
    )


def test_stock_item__image_sets_is_main(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.is_main
        == get_inventory_item_images_response["IsMain"]
    )


def test_stock_item__image_sets_sort_order(
    stock_item_image_with_response, get_inventory_item_images_response
):
    assert (
        stock_item_image_with_response.sort_order
        == get_inventory_item_images_response["SortOrder"]
    )
