from unittest.mock import call, patch

import pytest

from linnapi import exceptions, models, orders, requests


@pytest.fixture
def search_term():
    return "184165186"


@pytest.fixture
def processed_order_response():
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
        "PostalTrackingNumber": "JH47846456175GB",
        "cCountry": "United Kingdom",
        "Source": "EBAY",
        "PostalServiceName": "TPS: Royal Mail Tracked 48 - Non Signature",
        "ReferenceNum": "20-08658-40025",
        "SecondaryReference": "20-08658-40025",
        "ExternalReference": "1238579407101",
        "Address1": "59 Fake Drive",
        "Address2": "",
        "Address3": "",
        "Town": "Sometown",
        "Region": "Nowhere",
        "BuyerPhoneNumber": "999666999",
        "Company": "",
        "SubSource": "store",
        "ChannelBuyerName": "buyer",
        "AccountName": "Default",
        "cFullName": "Some Name",
        "cEmailAddress": "noone@nowhere.com",
        "cPostCode": "GUFF FFF",
        "dPaidOn": "2022-05-23T00:09:36Z",
        "dCancelledOn": "0001-01-01T00:00:00Z",
        "ItemWeight": 0.0,
        "TotalWeight": 0.0,
        "HoldOrCancel": False,
        "IsResend": False,
        "IsExchange": False,
        "TaxId": "",
        "FulfilmentLocationName": "Default",
    }


@pytest.fixture
def single_response(processed_order_response):
    return {
        "ProcessedOrders": {
            "PageNumber": 1,
            "EntriesPerPage": 100,
            "TotalEntries": 1,
            "TotalPages": 1,
            "Data": [processed_order_response],
        }
    }


@pytest.fixture
def multiple_response(single_response, processed_order_response):
    single_response["ProcessedOrders"]["Data"].extend(
        [processed_order_response, processed_order_response]
    )
    return single_response


@pytest.fixture
def mock_single_response(single_response):
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = single_response
        yield mock_make_request


@pytest.fixture
def mock_multiple_response(multiple_response):
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response
        yield mock_make_request


@pytest.fixture
def mock_multipage_response(multiple_response):
    multiple_response["ProcessedOrders"]["TotalPages"] = 3
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = multiple_response
        yield mock_make_request


@pytest.fixture
def mock_invalid_response():
    with patch("linnapi.orders.make_request") as mock_make_request:
        mock_make_request.return_value = {"invalid_key": "invalid_value"}
        yield mock_make_request


def test_search_processed_orders_makes_request(mock_single_response, search_term):
    orders.search_processed_orders(search_term)
    mock_single_response.called_once_with(
        orders.SearchProcessedOrders, search_term=search_term
    )


def test_search_processed_orders_single_return_value(mock_single_response, search_term):
    returned_value = orders.search_processed_orders(search_term)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 1
    assert isinstance(returned_value[0], models.ProcessedOrder)


def test_search_processed_orders_single_multiple_value(
    mock_multiple_response, search_term
):
    returned_value = orders.search_processed_orders(search_term)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 3
    assert all(
        (isinstance(value, models.ProcessedOrder) is True for value in returned_value)
    )


def test_search_processed_orders_with_multiple_pages_requests_all_pages(
    mock_multipage_response, search_term
):
    orders.search_processed_orders(search_term)
    mock_multipage_response.assert_has_calls(
        calls=(
            call(
                requests.orders.SearchProcessedOrders,
                search_term=search_term,
                page_number=1,
            ),
            call(
                requests.orders.SearchProcessedOrders,
                search_term=search_term,
                page_number=2,
            ),
            call(
                requests.orders.SearchProcessedOrders,
                search_term=search_term,
                page_number=3,
            ),
        )
    )
    mock_multipage_response.call_count == 3


def test_search_processed_orders_with_multiple_pages_returns_all_objects(
    mock_multipage_response, search_term
):
    returned_value = orders.search_processed_orders(search_term)
    assert len(returned_value) == 9


def test_search_processed_orders_with_invalid_response(
    mock_invalid_response, search_term
):
    with pytest.raises(exceptions.InvalidResponseError):
        orders.search_processed_orders(search_term)
