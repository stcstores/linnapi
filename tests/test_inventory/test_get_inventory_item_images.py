from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory, models
from linnapi.requests.inventory import GetInventoryItemImages


@pytest.fixture
def inventory_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def response_item():
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
def single_response(response_item):
    return [response_item]


@pytest.fixture
def multiple_response(response_item):
    return [response_item, response_item, response_item]


@pytest.fixture
def mock_single_response(single_response):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = single_response
        yield mock_make_request


@pytest.fixture
def mock_multiple_response(multiple_response):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = {"invalid_key": "invalid_value"}
        yield mock_make_request


def test_get_inventory_item_images_makes_request(
    mock_single_response, inventory_item_id
):
    inventory.get_inventory_item_images(inventory_item_id)
    mock_single_response.called_once_with(
        GetInventoryItemImages, inventory_item_id=inventory_item_id
    )


def test_get_inventory_item_images_single_return_value(
    mock_single_response, inventory_item_id
):
    returned_value = inventory.get_inventory_item_images(inventory_item_id)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 1
    assert isinstance(returned_value[0], models.StockItemImage)


def test_get_inventory_item_images_single_multiple_value(
    mock_multiple_response, inventory_item_id
):
    returned_value = inventory.get_inventory_item_images(inventory_item_id)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 3
    assert all(
        (isinstance(value, models.StockItemImage) is True for value in returned_value)
    )


def test_get_inventory_item_images_with_invalid_response(
    mock_invalid_response, inventory_item_id
):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_inventory_item_images(inventory_item_id)
