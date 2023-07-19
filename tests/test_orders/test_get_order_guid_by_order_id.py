from unittest.mock import Mock, patch

import pytest

from linnapi import exceptions, orders


@pytest.fixture
def order_id():
    return "98743579"


@pytest.fixture
def order_guid():
    return "73846ae8-9f64-42ef-8d76-31aa418da9d5"


@pytest.fixture
def mock_search_processed_orders(order_id, order_guid):
    with patch("linnapi.orders.search_processed_orders") as mock_search:
        mock_search.return_value = [Mock(order_id=order_id, order_guid=order_guid)]
        yield mock_search


@pytest.fixture
def mock_search_processed_orders_with_multiple_results(order_id, order_guid):
    with patch("linnapi.orders.search_processed_orders") as mock_search:
        mock_search.return_value = [
            Mock(order_id="116516516156", order_guid="616516515616"),
            Mock(order_id="161894165896", order_guid="89889489565"),
            Mock(order_id=order_id, order_guid=order_guid),
        ]
        yield mock_search


def test_get_order_guid_by_order_id_calls_search_processed_orders(
    mock_search_processed_orders, order_id
):
    orders.get_order_guid_by_order_id(order_id)
    mock_search_processed_orders.assert_called_once_with(search_term=order_id)


def test_get_order_guid_by_order_id_returns_order_guid(
    mock_search_processed_orders, order_id, order_guid
):
    assert orders.get_order_guid_by_order_id(order_id) == order_guid


def test_get_order_guid_by_order_id_accepts_ints(
    mock_search_processed_orders, order_id, order_guid
):
    orders.get_order_guid_by_order_id(int(order_id))
    mock_search_processed_orders.assert_called_once_with(search_term=order_id)


def test_get_order_guid_by_order_id_raises_when_no_orders_are_found(
    mock_search_processed_orders, order_id
):
    mock_search_processed_orders.return_value = []
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(int(order_id))
    assert str(excinfo.value) == "Search did not return any procesed orders."


def test_get_order_guid_by_order_id_raises_when_orders_are_returned_but_do_not_match_requested_order_id(
    mock_search_processed_orders, order_id, order_guid
):
    mock_search_processed_orders.return_value = [
        Mock(order_id="7403753402", order_guid=order_guid)
    ]
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(int(order_id))
    assert str(excinfo.value) == f"Order matching order ID {order_id} not found."


def test_get_order_guid_by_order_id_raises_when_multiple_orders_are_found(
    mock_search_processed_orders, order_id
):
    mock_search_processed_orders.return_value = [Mock(), Mock()]
    with pytest.raises(exceptions.InvalidResponseError) as excinfo:
        orders.get_order_guid_by_order_id(int(order_id))
    assert str(excinfo.value) == f"Order matching order ID {order_id} not found."


def test_get_order_guid_by_order_id_returns_order_guid_with_multiple_search_results(
    mock_search_processed_orders_with_multiple_results, order_id, order_guid
):
    assert orders.get_order_guid_by_order_id(order_id) == order_guid
