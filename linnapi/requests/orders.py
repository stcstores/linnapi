"""Orders requests."""

from typing import Any, MutableMapping

from linnapi.request import LinnworksAPIRequest


class SearchProcessedOrders(LinnworksAPIRequest):
    """Return details for a processed order."""

    URL = "https://eu-ext.linnworks.net/api/ProcessedOrders/SearchProcessedOrders"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        search_term: str = kwargs["search_term"]
        page_number: int = kwargs.get("page_number", 1)
        results_per_page: int = kwargs.get("results_per_page", 500)
        return {
            "request": {
                "SearchTerm": search_term,
                "PageNumber": page_number,
                "ResultsPerPage": results_per_page,
            }
        }


class GetProcessedAuditTrail(LinnworksAPIRequest):
    """Return the audit trail for a processed order."""

    URL = "https://eu-ext.linnworks.net/api/ProcessedOrders/GetProcessedAuditTrail"
    METHOD = LinnworksAPIRequest.GET

    @classmethod
    def params(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Return request URL parameters."""
        order_guid: str = kwargs["order_guid"]
        return {"pkOrderId": order_guid}

    @classmethod
    def headers(cls, *args: Any, **kwargs: Any) -> MutableMapping[str, str]:
        """Return request headers."""
        return {"accept": "application/json"}


class GetOrderDetailsByNumOrderId(LinnworksAPIRequest):
    """Return the details of a processed order by order ID."""

    URL = "https://eu-ext.linnworks.net/api/Orders/GetOrderDetailsByNumOrderId"
    METHOD = LinnworksAPIRequest.GET

    @classmethod
    def params(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Return request URL parameters."""
        order_id = str(kwargs["order_id"])
        return {"OrderId": order_id}
