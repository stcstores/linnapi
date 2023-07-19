from unittest.mock import Mock

import pytest

from linnapi.requests import orders


@pytest.fixture
def order_guid():
    return "73846ae8-9f64-42ef-8d76-31aa418da9d5"


def test_get_processed_audit_trail_url():
    url = "https://eu-ext.linnworks.net/api/ProcessedOrders/GetProcessedAuditTrail"
    assert orders.GetProcessedAuditTrail.URL == url


def test_get_processed_audit_trail_method():
    assert orders.GetProcessedAuditTrail.METHOD == "GET"


def test_get_processed_audit_trail_headers(order_guid):
    assert orders.GetProcessedAuditTrail.headers(order_guid=order_guid) == {
        "accept": "application/json"
    }


def test_get_processed_audit_trail_params(order_guid):
    expected_response = {"pkOrderId": order_guid}
    assert (
        orders.GetProcessedAuditTrail.params(order_guid=order_guid) == expected_response
    )


def test_get_processed_audit_trail_data(order_guid):
    assert orders.GetProcessedAuditTrail.data(order_guid=order_guid) is None


def test_get_processed_audit_trail_json(order_guid):
    assert orders.GetProcessedAuditTrail.json(order_guid=order_guid) is None


def test_get_processed_audit_trail_parse_response(order_guid):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        orders.GetProcessedAuditTrail.parse_response(response, order_guid=order_guid)
        == response.json.return_value
    )
