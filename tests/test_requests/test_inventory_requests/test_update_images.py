from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def image_id():
    return "eea21827-491d-4022-996a-d068dd6b25ea"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def sort_order():
    return 5


@pytest.fixture
def kwargs(image_id, stock_item_id, sort_order):
    return {
        "row_id": image_id,
        "stock_item_id": stock_item_id,
        "sort_order": sort_order,
        "is_main": True,
    }


def test_update_images_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/UpdateImages"
    assert inventory.UpdateImages.URL == url


def test_update_images_method():
    assert inventory.UpdateImages.METHOD == "POST"


def test_update_images_multi_headers(kwargs):
    assert inventory.UpdateImages.headers([kwargs]) == {}


def test_update_images_multi_params(kwargs):
    assert inventory.UpdateImages.params([kwargs]) is None


def test_update_images_multi_data(kwargs):
    assert inventory.UpdateImages.multi_data([kwargs]) is None


def test_update_images_multi_json(kwargs, stock_item_id, image_id, sort_order):
    expected_response = {
        "images": [
            {
                "pkRowId": image_id,
                "StockItemId": stock_item_id,
                "IsMain": True,
                "SortOrder": sort_order,
            }
        ]
    }
    assert inventory.UpdateImages.multi_json([kwargs]) == expected_response


def test_update_images_multi_json_with_multiple_requests(
    kwargs, stock_item_id, image_id, sort_order
):
    expected_response = {
        "images": [
            {
                "pkRowId": image_id,
                "StockItemId": stock_item_id,
                "IsMain": True,
                "SortOrder": sort_order,
            },
            {
                "pkRowId": image_id,
                "StockItemId": stock_item_id,
                "IsMain": True,
                "SortOrder": sort_order,
            },
            {
                "pkRowId": image_id,
                "StockItemId": stock_item_id,
                "IsMain": True,
                "SortOrder": sort_order,
            },
        ]
    }
    assert (
        inventory.UpdateImages.multi_json([kwargs, kwargs, kwargs]) == expected_response
    )


def test_update_images_multi_parse_response(kwargs):
    response = Mock()
    response.text = "Test Text"
    assert inventory.UpdateImages.parse_response(response, [kwargs]) == response.text
