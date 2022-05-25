import pytest

from linnapi import models


@pytest.fixture
def processed_order_data():
    return {
        "pkOrderID": "73846ae8-9f64-42ef-8d76-31aa418da9d5",
        "dReceivedDate": "2022-05-23T00:09:35Z",
        "dProcessedOn": "2022-05-23T07:25:47.19Z",
        "timeDiff": 0.30291886574074073,
        "fPostageCost": 0.0,
        "fTotalCharge": 27.99,
        "PostageCostExTax": 0.0,
        "Subtotal": 23.325,
        "fTax": 4.665,
        "TotalDiscount": 0.0,
        "ProfitMargin": 0.0,
        "CountryTaxRate": 20.0,
        "nOrderId": 109390,
        "nStatus": 1,
        "cCurrency": "GBP",
        "PostalTrackingNumber": "JH478881175GB",
        "cCountry": "United Kingdom",
        "Source": "EBAY",
        "PostalServiceName": "TPS: Royal Mail Tracked 48 - Non Signature",
        "ReferenceNum": "20-08658-40025",
        "SecondaryReference": "20-08658-40025",
        "ExternalReference": "1238579407101",
        "Address1": "59 Hawkesworth Drive",
        "Address2": "",
        "Address3": "",
        "Town": "Bagshot",
        "Region": "Surrey",
        "BuyerPhoneNumber": "07958381946",
        "Company": "",
        "SubSource": "stcstoresuk",
        "ChannelBuyerName": "jacksonsnotguilty",
        "AccountName": "Default",
        "cFullName": "Trevor  Jary",
        "cEmailAddress": "1445133baf1db7788294@members.ebay.com",
        "cPostCode": "GU19 5QY",
        "dPaidOn": "2022-05-23T00:09:36Z",
        "dCancelledOn": "2022-05-23T07:25:47.19Z",
        "ItemWeight": 0.0,
        "TotalWeight": 0.0,
        "HoldOrCancel": False,
        "IsResend": False,
        "IsExchange": False,
        "TaxId": "",
        "FulfilmentLocationName": "Default",
    }


@pytest.fixture
def uncancelled_cancellation_date():
    return "0001-01-01T00:00:00Z"


@pytest.fixture()
def processed_order(processed_order_data):
    return models.ProcessedOrder(processed_order_data)


@pytest.fixture()
def uncancelled_processed_order(processed_order_data, uncancelled_cancellation_date):
    processed_order_data["dCancelledOn"] = uncancelled_cancellation_date
    return models.ProcessedOrder(processed_order_data)


def test_processed_order_sets_raw(processed_order_data, processed_order):
    assert processed_order.raw == processed_order_data


def test_processed_order_sets_order_guid(processed_order_data, processed_order):
    assert processed_order.order_guid == processed_order_data["pkOrderID"]


def test_processed_order_sets_received_date(processed_order_data, processed_order):
    assert processed_order.received_date == models.parse_date_time(
        processed_order_data["dReceivedDate"]
    )


def test_processed_order_sets_processed_at(processed_order_data, processed_order):
    assert processed_order.processed_at == models.parse_date_time(
        processed_order_data["dProcessedOn"]
    )


def test_processed_order_sets_time_diff(processed_order_data, processed_order):
    assert processed_order.time_diff == processed_order_data["timeDiff"]


def test_processed_order_sets_postage_cost(processed_order_data, processed_order):
    assert processed_order.postage_cost == processed_order_data["fPostageCost"]


def test_processed_order_sets_total_charge(processed_order_data, processed_order):
    assert processed_order.total_charge == processed_order_data["fTotalCharge"]


def test_processed_order_sets_postage_cost_ex_tax(
    processed_order_data, processed_order
):
    assert (
        processed_order.postage_cost_ex_tax == processed_order_data["PostageCostExTax"]
    )


def test_processed_order_sets_subtotal(processed_order_data, processed_order):
    assert processed_order.subtotal == processed_order_data["Subtotal"]


def test_processed_order_sets_tax(processed_order_data, processed_order):
    assert processed_order.tax == processed_order_data["fTax"]


def test_processed_order_sets_total_discount(processed_order_data, processed_order):
    assert processed_order.total_discount == processed_order_data["TotalDiscount"]


def test_processed_order_sets_profit_margin(processed_order_data, processed_order):
    assert processed_order.profit_margin == processed_order_data["ProfitMargin"]


def test_processed_order_sets_country_tax_rate(processed_order_data, processed_order):
    assert processed_order.country_tax_rate == processed_order_data["CountryTaxRate"]


def test_processed_order_sets_order_id(processed_order_data, processed_order):
    assert processed_order.order_id == str(processed_order_data["nOrderId"])


def test_processed_order_sets_status_number(processed_order_data, processed_order):
    assert processed_order.status_number == processed_order_data["nStatus"]


def test_processed_order_sets_currency(processed_order_data, processed_order):
    assert processed_order.currency == processed_order_data["cCurrency"]


def test_processed_order_sets_tracking_number(processed_order_data, processed_order):
    assert (
        processed_order.tracking_number == processed_order_data["PostalTrackingNumber"]
    )


def test_processed_order_sets_country(processed_order_data, processed_order):
    assert processed_order.country == processed_order_data["cCountry"]


def test_processed_order_sets_source(processed_order_data, processed_order):
    assert processed_order.source == processed_order_data["Source"]


def test_processed_order_sets_subsource(processed_order_data, processed_order):
    assert processed_order.subsource == processed_order_data["SubSource"]


def test_processed_order_sets_postal_service(processed_order_data, processed_order):
    assert processed_order.postal_service == processed_order_data["PostalServiceName"]


def test_processed_order_sets_reference_number(processed_order_data, processed_order):
    assert processed_order.reference_number == processed_order_data["ReferenceNum"]


def test_processed_order_sets_secondary_reference(
    processed_order_data, processed_order
):
    assert (
        processed_order.secondary_reference
        == processed_order_data["SecondaryReference"]
    )


def test_processed_order_sets_external_reference(processed_order_data, processed_order):
    assert (
        processed_order.external_reference == processed_order_data["ExternalReference"]
    )


def test_processed_order_sets_address_1(processed_order_data, processed_order):
    assert processed_order.address_1 == processed_order_data["Address1"]


def test_processed_order_sets_address_2(processed_order_data, processed_order):
    assert processed_order.address_2 == processed_order_data["Address2"]


def test_processed_order_sets_address_3(processed_order_data, processed_order):
    assert processed_order.address_3 == processed_order_data["Address3"]


def test_processed_order_sets_town(processed_order_data, processed_order):
    assert processed_order.town == processed_order_data["Town"]


def test_processed_order_sets_region(processed_order_data, processed_order):
    assert processed_order.region == processed_order_data["Region"]


def test_processed_order_sets_buyer_phone_number(processed_order_data, processed_order):
    assert (
        processed_order.buyer_phone_number == processed_order_data["BuyerPhoneNumber"]
    )


def test_processed_order_sets_company(processed_order_data, processed_order):
    assert processed_order.company == processed_order_data["Company"]


def test_processed_order_sets_channel_buyer_namex(
    processed_order_data, processed_order
):
    assert (
        processed_order.channel_buyer_name == processed_order_data["ChannelBuyerName"]
    )


def test_processed_order_sets_account_name(processed_order_data, processed_order):
    assert processed_order.account_name == processed_order_data["AccountName"]


def test_processed_order_sets_customer_full_name(processed_order_data, processed_order):
    assert processed_order.customer_full_name == processed_order_data["cFullName"]


def test_processed_order_sets_customer_email_address(
    processed_order_data, processed_order
):
    assert (
        processed_order.customer_email_address == processed_order_data["cEmailAddress"]
    )


def test_processed_order_sets_customer_post_code(processed_order_data, processed_order):
    assert processed_order.customer_post_code == processed_order_data["cPostCode"]


def test_processed_order_sets_paid_at(processed_order_data, processed_order):
    assert processed_order.paid_at == models.parse_date_time(
        processed_order_data["dPaidOn"]
    )


def test_processed_order_sets_cancelled_at(processed_order_data, processed_order):
    assert processed_order.cancelled_at == models.parse_date_time(
        processed_order_data["dCancelledOn"]
    )


def test_processed_order_sets_cancelled_at_to_none_when_order_is_not_cancelled(
    processed_order_data, uncancelled_processed_order
):
    assert uncancelled_processed_order.cancelled_at is None


def test_processed_order_sets_item_weight(processed_order_data, processed_order):
    assert processed_order.item_weight == processed_order_data["ItemWeight"]


def test_processed_order_sets_total_weight(processed_order_data, processed_order):
    assert processed_order.total_weight == processed_order_data["TotalWeight"]


def test_processed_order_sets_hold_or_cancel(processed_order_data, processed_order):
    assert processed_order.hold_or_cancel == processed_order_data["HoldOrCancel"]


def test_processed_order_sets_is_resend(processed_order_data, processed_order):
    assert processed_order.is_resend == processed_order_data["IsResend"]


def test_processed_order_sets_is_exchange(processed_order_data, processed_order):
    assert processed_order.is_exchange == processed_order_data["IsExchange"]


def test_processed_order_sets_tax_id(processed_order_data, processed_order):
    assert processed_order.tax_id == processed_order_data["TaxId"]


def test_processed_order_sets_fulfilment_location_name(
    processed_order_data, processed_order
):
    assert (
        processed_order.fulfilment_location_name
        == processed_order_data["FulfilmentLocationName"]
    )
