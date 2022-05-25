import pytest

from linnapi import models


@pytest.fixture
def order_audit_trail_data():
    return {
        "sid_history": 53825,
        "fkOrderId": "73846ae8-9f64-42ef-8d76-31aa418da9d5",
        "HistoryNote": "Order line MAY-YVP-78Y sent to store",
        "fkOrderHistoryTypeId": "DESPATCH_NOTE",
        "DateStamp": "2022-05-23T07:27:54.903Z",
        "Tag": "CONFIRMED",
        "UpdatedBy": "SYNC",
        "TypeDescription": "Dispatch note has been sent to channel",
    }


@pytest.fixture()
def order_audit_trail_entry_with_data(order_audit_trail_data):
    return models.OrderAuditTrailEntry(order_audit_trail_data)


def test_order_audit_trail_entry_sets_raw(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert order_audit_trail_entry_with_data.raw == order_audit_trail_data


def test_order_audit_trail_entry_sets_history_id(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert (
        order_audit_trail_entry_with_data.history_id
        == order_audit_trail_data["sid_history"]
    )


def test_order_audit_trail_entry_sets_order_guid(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert (
        order_audit_trail_entry_with_data.order_guid
        == order_audit_trail_data["fkOrderId"]
    )


def test_order_audit_trail_entry_sets_history_note(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert (
        order_audit_trail_entry_with_data.history_note
        == order_audit_trail_data["HistoryNote"]
    )


def test_order_audit_trail_entry_sets_timestamp(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert order_audit_trail_entry_with_data.timestamp == models.parse_date_time(
        order_audit_trail_data["DateStamp"]
    )


def test_order_audit_trail_entry_sets_tag(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert order_audit_trail_entry_with_data.tag == order_audit_trail_data["Tag"]


def test_order_audit_trail_entry_sets_updated_by(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert (
        order_audit_trail_entry_with_data.updated_by
        == order_audit_trail_data["UpdatedBy"]
    )


def test_order_audit_trail_entry_sets_type_description(
    order_audit_trail_data, order_audit_trail_entry_with_data
):
    assert (
        order_audit_trail_entry_with_data.type_description
        == order_audit_trail_data["TypeDescription"]
    )
