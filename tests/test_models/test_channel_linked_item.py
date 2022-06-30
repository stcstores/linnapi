import pytest

from linnapi import models


@pytest.fixture
def channel_skus_response():
    return {
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
    }


@pytest.fixture
def channel_linked_item(channel_skus_response):
    return models.ChannelLinkedItem(channel_skus_response)


def test_channel_linked_item_sets_raw(channel_linked_item, channel_skus_response):
    assert channel_linked_item.raw == channel_skus_response


def test_channel_linked_item_sets_channel_sku_id(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.channel_sku_id == channel_skus_response["ChannelSKURowId"]
    )


def test_channel_linked_item_sets_sku(channel_linked_item, channel_skus_response):
    assert channel_linked_item.sku == channel_skus_response["SKU"]


def test_channel_linked_item_sets_source(channel_linked_item, channel_skus_response):
    assert channel_linked_item.source == channel_skus_response["Source"]


def test_channel_linked_item_sets_sub_source(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.sub_source == channel_skus_response["SubSource"]


def test_channel_linked_item_sets_update_status(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.update_status == channel_skus_response["UpdateStatus"]


def test_channel_linked_item_sets_channel_reference_id(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.channel_reference_id
        == channel_skus_response["ChannelReferenceId"]
    )


def test_channel_linked_item_sets_last_update(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.last_update == models.parse_date_time(
        channel_skus_response["LastUpdate"]
    )


def test_channel_linked_item_sets_max_listed_quantity(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.max_listed_quantity
        == channel_skus_response["MaxListedQuantity"]
    )


def test_channel_linked_item_sets_end_when_stock(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.end_when_stock == channel_skus_response["EndWhenStock"]


def test_channel_linked_item_sets_submitted_quantity(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.submitted_quantity
        == channel_skus_response["SubmittedQuantity"]
    )


def test_channel_linked_item_sets_listed_quantity(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.listed_quantity == channel_skus_response["ListedQuantity"]
    )


def test_channel_linked_item_sets_stock_percentage(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.stock_percentage == channel_skus_response["StockPercentage"]
    )


def test_channel_linked_item_sets_ignore_sync(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.ignore_sync == channel_skus_response["IgnoreSync"]


def test_channel_linked_item_sets_is_multi_location(
    channel_linked_item, channel_skus_response
):
    assert (
        channel_linked_item.is_multi_location
        == channel_skus_response["IsMultiLocation"]
    )


def test_channel_linked_item_sets_stock_item_id(
    channel_linked_item, channel_skus_response
):
    assert channel_linked_item.stock_item_id == channel_skus_response["StockItemId"]
