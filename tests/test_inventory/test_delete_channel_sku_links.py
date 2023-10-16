from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory
from linnapi.requests.inventory import DeleteInventoryItemChannelSKUs


@pytest.fixture
def channel_item_id():
    return "965c4c47-227d-4b87-913f-0114dab13b61"


@pytest.fixture
def channel_item_ids():
    return [
        "d28efd06-57c4-4792-9048-50c31264acd3",
        "69a73aa0-f504-4f9a-ae59-13f6aae38279",
        "4a692c35-ef6c-4fde-9387-69a52625c7e6",
    ]


@pytest.fixture
def mock_success_response():
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = True
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = False
        yield mock_make_request


def test_return_value(mock_success_response, channel_item_id):
    returned_value = inventory.delete_channel_sku_links([channel_item_id])
    assert returned_value is None


def test_makes_request(mock_success_response, channel_item_id):
    inventory.delete_channel_sku_links([channel_item_id])
    mock_success_response.assert_called_once_with(
        DeleteInventoryItemChannelSKUs,
        inventory_item_channel_sku_ids=([channel_item_id],),
    )


def test_makes_request_with_multiple_channel_ids(
    mock_success_response, channel_item_ids
):
    inventory.delete_channel_sku_links(*channel_item_ids)
    mock_success_response.assert_called_once_with(
        DeleteInventoryItemChannelSKUs,
        inventory_item_channel_sku_ids=tuple(channel_item_ids),
    )


def test_invalid_response(mock_invalid_response):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.delete_channel_sku_links([channel_item_id])
