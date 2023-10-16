from unittest.mock import patch

import pytest

from linnapi import inventory, models


@pytest.fixture
def skus():
    return ["SKU_1", "SKU_2", "SKU_3"]


@pytest.fixture
def stock_item_ids():
    return [
        "d28efd06-57c4-4792-9048-50c31264acd3",
        "69a73aa0-f504-4f9a-ae59-13f6aae38279",
        "4a692c35-ef6c-4fde-9387-69a52625c7e6",
    ]


@pytest.fixture
def get_stock_item_ids_by_sku_return_value(skus, stock_item_ids):
    return dict(zip(skus, stock_item_ids))


@pytest.fixture
def get_item_channel_skus_response():
    return {
        "d28efd06-57c4-4792-9048-50c31264acd3": [
            models.ChannelLinkedItem(
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
                }
            )
        ],
        "69a73aa0-f504-4f9a-ae59-13f6aae38279": [
            models.ChannelLinkedItem(
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
                }
            ),
        ],
        "4a692c35-ef6c-4fde-9387-69a52625c7e6": [
            models.ChannelLinkedItem(
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
                }
            ),
        ],
    }


@pytest.fixture
def mock_get_stock_item_ids_by_sku(get_stock_item_ids_by_sku_return_value):
    with patch(
        "linnapi.inventory.get_stock_item_ids_by_sku"
    ) as mock_get_stock_item_ids_by_sku:
        mock_get_stock_item_ids_by_sku.return_value = (
            get_stock_item_ids_by_sku_return_value
        )
        yield mock_get_stock_item_ids_by_sku


@pytest.fixture
def mock_get_item_channel_skus(get_item_channel_skus_response):
    with patch("linnapi.inventory.get_item_channel_skus") as mock_get_item_channel_skus:
        mock_get_item_channel_skus.return_value = get_item_channel_skus_response
        yield mock_get_item_channel_skus


def test_get_channel_skus_by_skus_calls_get_stock_item_ids_by_sku(
    mock_get_stock_item_ids_by_sku, mock_get_item_channel_skus, skus
):
    inventory.get_channel_skus_by_skus(*skus)
    mock_get_stock_item_ids_by_sku.assert_called_once_with(*skus)


def test_get_channel_skus_by_skus_calls_get_item_channel_skus(
    mock_get_stock_item_ids_by_sku, mock_get_item_channel_skus, skus, stock_item_ids
):
    inventory.get_channel_skus_by_skus(*skus)
    mock_get_item_channel_skus.assert_called_once_with(*stock_item_ids)


def test_get_channel_skus_by_skus_return_value(
    mock_get_stock_item_ids_by_sku,
    mock_get_item_channel_skus,
    skus,
    stock_item_ids,
    get_item_channel_skus_response,
):
    returned_value = inventory.get_channel_skus_by_skus(*skus)
    assert isinstance(returned_value, dict)
    assert list(returned_value.keys()) == skus
    assert returned_value[skus[0]] == get_item_channel_skus_response[stock_item_ids[0]]
