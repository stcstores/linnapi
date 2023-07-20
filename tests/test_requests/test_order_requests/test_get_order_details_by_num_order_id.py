from unittest.mock import Mock

import pytest

from linnapi.requests import orders


@pytest.fixture
def order_id():
    return "73846ae8-9f64-42ef-8d76-31aa418da9d5"


def test_get_processed_audit_trail_url():
    url = "https://eu-ext.linnworks.net/api/Orders/GetOrderDetailsByNumOrderId"
    assert orders.GetOrderDetailsByNumOrderId.URL == url


def test_get_processed_audit_trail_method():
    assert orders.GetOrderDetailsByNumOrderId.METHOD == "GET"


def test_get_processed_audit_trail_headers(order_id):
    assert orders.GetOrderDetailsByNumOrderId.headers(order_id=order_id) == {}


def test_get_processed_audit_trail_params(order_id):
    expected_response = {"OrderId": order_id}
    assert (
        orders.GetOrderDetailsByNumOrderId.params(order_id=order_id)
        == expected_response
    )


def test_get_processed_audit_trail_data(order_id):
    assert orders.GetOrderDetailsByNumOrderId.data(order_id=order_id) is None


def test_get_processed_audit_trail_json(order_id):
    assert orders.GetOrderDetailsByNumOrderId.json(order_id=order_id) is None


def test_get_processed_audit_trail_parse_response(order_id):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        orders.GetOrderDetailsByNumOrderId.parse_response(response, order_id=order_id)
        == response.json.return_value
    )
