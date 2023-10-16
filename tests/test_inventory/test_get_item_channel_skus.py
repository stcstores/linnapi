from unittest.mock import patch

import pytest

from linnapi import exceptions, inventory, models
from linnapi.requests.inventory import BatchGetInventoryItemChannelSKUs


@pytest.fixture
def stock_item_id():
    return "8f8ec9eb-07d0-4bf5-94a0-a4a9c2c7f2ad"


@pytest.fixture
def stock_item_ids():
    return [
        "d28efd06-57c4-4792-9048-50c31264acd3",
        "69a73aa0-f504-4f9a-ae59-13f6aae38279",
        "4a692c35-ef6c-4fde-9387-69a52625c7e6",
    ]


@pytest.fixture
def response_data():
    return [
        {
            "StockItemId": "8f8ec9eb-07d0-4bf5-94a0-a4a9c2c7f2ad",
            "ChannelSkus": [
                {
                    "ChannelSKURowId": "8e93e431-5c35-42ce-8e2c-a693cece6b33",
                    "SKU": "C6-8OIO-RBT8",
                    "Source": "AMAZON",
                    "SubSource": "Amazon Canada",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "B0028RDINY",
                    "LastUpdate": "2022-06-29T21:14:08.843Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 30,
                    "ListedQuantity": 30,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "8f8ec9eb-07d0-4bf5-94a0-a4a9c2c7f2ad",
                    "StockItemIntId": 0,
                },
                {
                    "ChannelSKURowId": "35173080-f1c9-4bd3-96bf-dd5325e0b907",
                    "SKU": "C6-8OIO-RBT8",
                    "Source": "AMAZON",
                    "SubSource": "Amazon USA",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "B0028RDINY",
                    "LastUpdate": "2022-06-29T21:14:07.353Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 1079,
                    "ListedQuantity": 1079,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "8f8ec9eb-07d0-4bf5-94a0-a4a9c2c7f2ad",
                    "StockItemIntId": 0,
                },
                {
                    "ChannelSKURowId": "e2e7586d-8af3-45bd-901b-1e59cc209876",
                    "SKU": "VYD-AK2-VNC",
                    "Source": "AMAZON",
                    "SubSource": "Amazon Mexico",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "",
                    "LastUpdate": "2022-06-29T21:14:09.187Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 30,
                    "ListedQuantity": 30,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "8f8ec9eb-07d0-4bf5-94a0-a4a9c2c7f2ad",
                    "StockItemIntId": 0,
                },
            ],
        }
    ]


@pytest.fixture
def multiple_response_data():
    return [
        {
            "StockItemId": "d28efd06-57c4-4792-9048-50c31264acd3",
            "ChannelSkus": [
                {
                    "ChannelSKURowId": "8e93e431-5c35-42ce-8e2c-a693cece6b33",
                    "SKU": "C6-8OIO-RBT8",
                    "Source": "AMAZON",
                    "SubSource": "Amazon Canada",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "B0028RDINY",
                    "LastUpdate": "2022-06-29T21:14:08.843Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 30,
                    "ListedQuantity": 30,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "d28efd06-57c4-4792-9048-50c31264acd3",
                    "StockItemIntId": 0,
                },
            ],
        },
        {
            "StockItemId": "69a73aa0-f504-4f9a-ae59-13f6aae38279",
            "ChannelSkus": [
                {
                    "ChannelSKURowId": "35173080-f1c9-4bd3-96bf-dd5325e0b907",
                    "SKU": "C6-8OIO-RBT8",
                    "Source": "AMAZON",
                    "SubSource": "Amazon USA",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "B0028RDINY",
                    "LastUpdate": "2022-06-29T21:14:07.353Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 1079,
                    "ListedQuantity": 1079,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "69a73aa0-f504-4f9a-ae59-13f6aae38279",
                    "StockItemIntId": 0,
                },
            ],
        },
        {
            "StockItemId": "4a692c35-ef6c-4fde-9387-69a52625c7e6",
            "ChannelSkus": [
                {
                    "ChannelSKURowId": "e2e7586d-8af3-45bd-901b-1e59cc209876",
                    "SKU": "VYD-AK2-VNC",
                    "Source": "AMAZON",
                    "SubSource": "Amazon Mexico",
                    "UpdateStatus": "Confirmed",
                    "ChannelReferenceId": "",
                    "LastUpdate": "2022-06-29T21:14:09.187Z",
                    "MaxListedQuantity": 0,
                    "EndWhenStock": 0,
                    "SubmittedQuantity": 30,
                    "ListedQuantity": 30,
                    "StockPercentage": 0.0,
                    "IgnoreSync": False,
                    "IsMultiLocation": False,
                    "StockItemId": "4a692c35-ef6c-4fde-9387-69a52625c7e6",
                    "StockItemIntId": 0,
                },
            ],
        },
    ]


@pytest.fixture
def mock_single_response(response_data):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = response_data
        yield mock_make_request


@pytest.fixture
def mock_multiple_response(multiple_response_data):
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response_data
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.inventory.make_request") as mock_make_request:
        mock_make_request.return_value = {"invalid_key": "invalid_value"}
        yield mock_make_request


def test_get_item_channel_skus_return_value(
    mock_single_response, response_data, stock_item_id
):
    returned_value = inventory.get_item_channel_skus(stock_item_id)
    assert isinstance(returned_value, dict)
    assert list(returned_value.keys()) == [stock_item_id]
    assert isinstance(returned_value[stock_item_id], list)
    for i, item in enumerate(returned_value[stock_item_id]):
        assert isinstance(item, models.ChannelLinkedItem)
        assert item.sku == response_data[0]["ChannelSkus"][i]["SKU"]


def test_get_item_channel_skus_makes_request(mock_single_response, stock_item_id):
    inventory.get_item_channel_skus(stock_item_id)
    mock_single_response.assert_called_once_with(
        BatchGetInventoryItemChannelSKUs, stock_item_ids=(stock_item_id,)
    )


def test_get_item_channel_skus_makes_request_with_multiple_skus(
    mock_multiple_response, stock_item_ids
):
    inventory.get_item_channel_skus(stock_item_ids)
    mock_multiple_response.assert_called_once_with(
        BatchGetInventoryItemChannelSKUs, stock_item_ids=(stock_item_ids,)
    )


def test_get_item_channel_skus_return_value_multiple_skus(
    mock_multiple_response, multiple_response_data, stock_item_ids
):
    returned_value = inventory.get_item_channel_skus(stock_item_ids)
    assert isinstance(returned_value, dict)
    assert list(returned_value.keys()) == stock_item_ids
    for item_index, stock_item_id in enumerate(stock_item_ids):
        assert isinstance(returned_value[stock_item_id], list)
        for channel_sku_index, item in enumerate(returned_value[stock_item_id]):
            assert isinstance(item, models.ChannelLinkedItem)
            item_sku = multiple_response_data[item_index]["ChannelSkus"][
                channel_sku_index
            ]["SKU"]
            assert item.sku == item_sku


def test_get_item_channel_skus_invalid_response(mock_invalid_response, stock_item_ids):
    with pytest.raises(exceptions.InvalidResponseError):
        inventory.get_item_channel_skus(*stock_item_ids)
