import datetime as dt

import pytest

from linnapi import models


@pytest.fixture
def get_stock_level_response():
    return {
        "Location": {
            "StockLocationId": "00000000-0000-0000-0000-000000000000",
            "StockLocationIntId": 0,
            "LocationName": "Default",
            "IsFulfillmentCenter": False,
            "IsWarehouseManaged": False,
        },
        "StockLevel": 3,
        "StockValue": 0.0,
        "MinimumLevel": 4,
        "InOrderBook": 0,
        "Due": 0,
        "JIT": False,
        "InOrders": 0,
        "Available": 3,
        "UnitCost": 0.0,
        "SKU": "E32-99X-8G2",
        "AutoAdjust": True,
        "LastUpdateDate": "2022-03-15T14:31:09.103Z",
        "LastUpdateOperation": "DIRECT ADJUSTMENT BY stcadmin",
        "rowid": "2df49516-77f7-4eb6-aa75-dd6ae9ec7e82",
        "PendingUpdate": False,
        "StockItemPurchasePrice": 9.6,
        "StockItemId": "965c4c47-227d-4b87-913f-0114dab13b61",
        "StockItemIntId": 0,
    }


@pytest.fixture
def set_stock_level_response():
    return {
        "Location": {
            "StockLocationId": "00000000-0000-0000-0000-000000000000",
            "StockLocationIntId": 0,
            "LocationName": "Default",
            "IsFulfillmentCenter": False,
        },
        "StockLevel": 0,
        "StockValue": 0.0,
        "MinimumLevel": 4,
        "InOrderBook": 0,
        "Due": 0,
        "JIT": False,
        "InOrders": 0,
        "Available": 0,
        "UnitCost": 9.6,
        "SKU": "E32-99X-8G2",
        "AutoAdjust": True,
        "LastUpdateDate": "2022-03-18T15:22:06.273Z",
        "LastUpdateOperation": "DIRECT ADJUSTMENT BY stcadmin",
        "rowid": "2df49516-77f7-4eb6-aa75-dd6ae9ec7e82",
        "PendingUpdate": False,
        "StockItemPurchasePrice": 9.6,
        "StockItemId": "965c4c47-227d-4b87-913f-0114dab13b61",
        "StockItemIntId": 0,
    }


@pytest.fixture
def stock_level_info_with_get_stock_level_response(get_stock_level_response):
    return models.StockLevelInfo(get_stock_level_response)


@pytest.fixture
def stock_level_info_with_set_stock_level_response(set_stock_level_response):
    return models.StockLevelInfo(set_stock_level_response)


def test_stock_level_info_with_get_stock_level_response_parse_date_time_method(
    get_stock_level_response,
):
    date_string = get_stock_level_response["LastUpdateDate"]
    date = dt.datetime(
        year=2022, month=3, day=15, hour=14, minute=31, second=9, microsecond=103000
    )
    assert models.StockLevelInfo.parse_date_time(date_string) == date


def test_stock_level_info_with_get_stock_level_response_sets_raw(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.raw == get_stock_level_response
    )


def test_stock_level_info_with_get_stock_level_response_sets_auto_adjust(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.auto_adjust
        == get_stock_level_response["AutoAdjust"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_available(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.available
        == get_stock_level_response["Available"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_due(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.due
        == get_stock_level_response["Due"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_in_order_book(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.in_order_book
        == get_stock_level_response["InOrderBook"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_in_orders(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.in_orders
        == get_stock_level_response["InOrders"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_jit(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.jit
        == get_stock_level_response["JIT"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_last_update_date(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.last_update_date
        == models.StockLevelInfo.parse_date_time(
            get_stock_level_response["LastUpdateDate"]
        )
    )


def test_stock_level_info_with_get_stock_level_response_sets_last_update_operation(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.last_update_operation
        == get_stock_level_response["LastUpdateOperation"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_location_is_fulfillment_center(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.location_is_fulfillment_center
        == get_stock_level_response["Location"]["IsFulfillmentCenter"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_location_is_warehouse_managed(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.location_is_warehouse_managed
        == get_stock_level_response["Location"]["IsWarehouseManaged"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_location_name(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.location_name
        == get_stock_level_response["Location"]["LocationName"]
    )


def test_stock_level_info_with_get_stock_level_response_sets_location_id(
    stock_level_info_with_get_stock_level_response, get_stock_level_response
):
    assert (
        stock_level_info_with_get_stock_level_response.location_id
        == get_stock_level_response["Location"]["StockLocationId"]
    )


def test_stock_level_info_with_set_stock_level_response_parse_date_time_method(
    set_stock_level_response,
):
    date_string = set_stock_level_response["LastUpdateDate"]
    date = dt.datetime(2022, 3, 18, 15, 22, 6, 273000)
    assert models.StockLevelInfo.parse_date_time(date_string) == date


def test_stock_level_info_with_set_stock_level_response_sets_raw(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.raw == set_stock_level_response
    )


def test_stock_level_info_with_set_stock_level_response_sets_auto_adjust(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.auto_adjust
        == set_stock_level_response["AutoAdjust"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_available(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.available
        == set_stock_level_response["Available"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_due(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.due
        == set_stock_level_response["Due"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_in_order_book(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.in_order_book
        == set_stock_level_response["InOrderBook"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_in_orders(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.in_orders
        == set_stock_level_response["InOrders"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_jit(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.jit
        == set_stock_level_response["JIT"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_last_update_date(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.last_update_date
        == models.StockLevelInfo.parse_date_time(
            set_stock_level_response["LastUpdateDate"]
        )
    )


def test_stock_level_info_with_set_stock_level_response_sets_last_update_operation(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.last_update_operation
        == set_stock_level_response["LastUpdateOperation"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_location_is_fulfillment_center(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.location_is_fulfillment_center
        == set_stock_level_response["Location"]["IsFulfillmentCenter"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_location_is_warehouse_managed(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.location_is_warehouse_managed
        is None
    )


def test_stock_level_info_with_set_stock_level_response_sets_location_name(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.location_name
        == set_stock_level_response["Location"]["LocationName"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_location_id(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.location_id
        == set_stock_level_response["Location"]["StockLocationId"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_location_int_id(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.location_int_id
        == set_stock_level_response["Location"]["StockLocationIntId"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_minimum_level(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.minimum_level
        == set_stock_level_response["MinimumLevel"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_pending_update(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.pending_update
        == set_stock_level_response["PendingUpdate"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_sku(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.sku
        == set_stock_level_response["SKU"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_stock_item_id(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.stock_item_id
        == set_stock_level_response["StockItemId"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_stock_item_int_id(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.stock_item_int_id
        == set_stock_level_response["StockItemIntId"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_stock_item_purchase_price(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.stock_item_purchase_price
        == set_stock_level_response["StockItemPurchasePrice"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_stock_level(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.stock_level
        == set_stock_level_response["StockLevel"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_stock_value(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.stock_value
        == set_stock_level_response["StockValue"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_unit_cost(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.unit_cost
        == set_stock_level_response["UnitCost"]
    )


def test_stock_level_info_with_set_stock_level_response_sets_row_id(
    stock_level_info_with_set_stock_level_response, set_stock_level_response
):
    assert (
        stock_level_info_with_set_stock_level_response.row_id
        == set_stock_level_response["rowid"]
    )
