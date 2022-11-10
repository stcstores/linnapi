from unittest.mock import Mock

import pytest

from linnapi.requests import inventory


@pytest.fixture
def channel_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def kwargs(channel_item_id):
    return {"inventory_item_channel_sku_ids": [channel_item_id]}


def test_url():
    url = "https://eu-ext.linnworks.net/api/Inventory/DeleteInventoryItemChannelSKUs"
    assert inventory.DeleteInventoryItemChannelSKUs.URL == url


def test_method():
    assert inventory.DeleteInventoryItemChannelSKUs.METHOD == "POST"


def test_headers(kwargs):
    assert inventory.DeleteInventoryItemChannelSKUs.headers(kwargs) == {}


def test_params(kwargs):
    assert inventory.DeleteInventoryItemChannelSKUs.params(kwargs) is None


def test_data(kwargs):
    assert inventory.DeleteInventoryItemChannelSKUs.data(kwargs) is None


def test_json_with_single_arg(kwargs, channel_item_id):
    expected_response = {"inventoryItemChannelSKUIds": [channel_item_id]}
    assert (
        inventory.DeleteInventoryItemChannelSKUs.json(
            inventory_item_channel_sku_ids=[channel_item_id]
        )
        == expected_response
    )


def test_json_with_single_multiple_args():
    channel_item_ids = [
        "b6fcbf79-c827-4802-9974-3727a3658f41",
        "094b4815-4987-475c-8e57-fca8f46b02a9",
        "972af264-d768-4c6c-9152-0ad9d9d5b352",
    ]
    expected_response = {"inventoryItemChannelSKUIds": channel_item_ids}
    assert (
        inventory.DeleteInventoryItemChannelSKUs.json(
            inventory_item_channel_sku_ids=channel_item_ids
        )
        == expected_response
    )


@pytest.mark.parametrize(
    "status_code,expected",
    [(204, True), (200, False), (404, False), (500, False), (501, False)],
)
def test_parse_response(status_code, expected):
    response = Mock(status_code=status_code)
    assert inventory.DeleteInventoryItemChannelSKUs.parse_response(response) is expected
