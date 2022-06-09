import pytest

from linnapi import models


@pytest.fixture
def stock_item_history_data():
    return {
        "Date": "2022-04-11T13:32:10.993Z",
        "Level": 44,
        "StockValue": 0.0,
        "Note": "Imported from file",
        "ChangeQty": 44,
        "ChangeValue": 0.0,
        "StockItemId": "6079faa4-e4ff-4b5b-9990-fc571e70412e",
        "StockItemIntId": 0,
    }


@pytest.fixture()
def stock_item_history(stock_item_history_data):
    return models.StockItemHistoryRecord(stock_item_history_data)


def test_stock_item_history_sets_raw(stock_item_history_data, stock_item_history):
    assert stock_item_history.raw == stock_item_history_data


def test_stock_item_history_sets_timestamp(stock_item_history_data, stock_item_history):
    assert stock_item_history.timestamp == models.parse_date_time(
        stock_item_history_data["Date"]
    )


def test_stock_item_history_sets_stock_level(
    stock_item_history_data, stock_item_history
):
    assert stock_item_history.stock_level == stock_item_history_data["Level"]


def test_stock_item_history_sets_text(stock_item_history_data, stock_item_history):
    assert stock_item_history.text == stock_item_history_data["Note"]


def test_stock_item_history_sets_relative_change(
    stock_item_history_data, stock_item_history
):
    assert stock_item_history.relative_change == stock_item_history_data["ChangeQty"]


def test_stock_item_history_sets_stock_item_id(
    stock_item_history_data, stock_item_history
):
    assert stock_item_history.stock_item_id == stock_item_history_data["StockItemId"]
