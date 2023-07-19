"""Methods for interacting with Linnworks orders."""

from linnapi import exceptions, models
from linnapi.request import make_request
from linnapi.requests.orders import GetProcessedAuditTrail, SearchProcessedOrders


def search_processed_orders(search_term: str) -> list[models.ProcessedOrder]:
    """Return a search for processed orders."""
    page_number = 1
    total_pages = 2
    processed_orders = []
    while page_number <= total_pages:
        response = make_request(
            SearchProcessedOrders, search_term=search_term, page_number=page_number
        )
        try:
            total_pages = response["ProcessedOrders"]["TotalPages"]
            processed_orders.extend(
                [
                    models.ProcessedOrder(order)
                    for order in response["ProcessedOrders"]["Data"]
                ]
            )
        except (KeyError, IndexError, TypeError):
            raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
        else:
            page_number += 1
    return processed_orders


def get_order_guid_by_order_id(order_id: str) -> str:
    """Return the GUID id for an order by order ID."""
    search_results = search_processed_orders(search_term=str(order_id))
    if len(search_results) == 0:
        raise exceptions.InvalidResponseError(
            "Search did not return any procesed orders."
        )
    for order in search_results:
        if str(order.order_id) == str(order_id):
            return str(order.order_guid)
    raise exceptions.InvalidResponseError(
        f"Order matching order ID {order_id} not found."
    )


def get_processed_order_audit_trail(
    order_guid: str,
) -> list[models.OrderAuditTrailEntry]:
    """Return the the audit trail for a processed order."""
    response = make_request(GetProcessedAuditTrail, order_guid=order_guid)
    try:
        audit_trail = [models.OrderAuditTrailEntry(entry) for entry in response]
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return audit_trail
