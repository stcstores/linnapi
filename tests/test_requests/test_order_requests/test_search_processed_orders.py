from unittest.mock import Mock

import pytest

from linnapi.requests import orders


@pytest.fixture
def search_term():
    return "89468168"


def test_search_processed_orders_url():
    url = "https://eu-ext.linnworks.net/api/ProcessedOrders/SearchProcessedOrders"
    assert orders.SearchProcessedOrders.URL == url


def test_search_processed_orders_method():
    assert orders.SearchProcessedOrders.METHOD == "POST"


def test_search_processed_orders_headers(search_term):
    assert orders.SearchProcessedOrders.headers(search_term=search_term) == {}


def test_search_processed_orders_params(search_term):
    assert orders.SearchProcessedOrders.params(search_term=search_term) is None


def test_search_processed_orders_data(search_term):
    assert orders.SearchProcessedOrders.data(search_term=search_term) is None


def test_search_processed_orders_json(search_term):
    expected_response = {
        "request": {
            "SearchTerm": search_term,
            "PageNumber": 1,
            "ResultsPerPage": 100,
        }
    }
    assert (
        orders.SearchProcessedOrders.json(search_term=search_term) == expected_response
    )


def test_search_processed_orders_json_with_page_number(search_term):
    expected_response = {
        "request": {
            "SearchTerm": search_term,
            "PageNumber": 5,
            "ResultsPerPage": 100,
        }
    }
    assert (
        orders.SearchProcessedOrders.json(search_term=search_term, page_number=5)
        == expected_response
    )


def test_search_processed_orders_json_with_results_per_page(search_term):
    expected_response = {
        "request": {
            "SearchTerm": search_term,
            "PageNumber": 1,
            "ResultsPerPage": 5,
        }
    }
    assert (
        orders.SearchProcessedOrders.json(search_term=search_term, results_per_page=5)
        == expected_response
    )


def test_search_processed_orders_parse_response(search_term):
    response = Mock()
    response.json.return_value = {"key": "value"}
    assert (
        orders.SearchProcessedOrders.parse_response(response, search_term=search_term)
        == response.json.return_value
    )
