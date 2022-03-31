"""Inventory requests."""

from typing import Any

from linnapi.request import LinnworksAPIRequest


class GetStockItemIDsBySKU(LinnworksAPIRequest):
    """Return the stock item ID for a SKU."""

    URL = "https://eu-ext.linnworks.net/api/Inventory/GetStockItemIdsBySKU"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        skus: list[str] = kwargs["skus"]
        return {"request": {"SKUS": skus}}


class GetStockLevel(LinnworksAPIRequest):
    """Return the current stock level for a product by stock item ID."""

    URL = "https://eu-ext.linnworks.net/api/Stock/GetStockLevel"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        stock_item_id: str = kwargs["stock_item_id"]
        return {"stockItemId": stock_item_id}


class GetStockLevelBatch(LinnworksAPIRequest):
    """Return the stock level for multiple products by stock item ID."""

    URL = "https://eu-ext.linnworks.net/api/Stock/GetStockLevel_Batch"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        stock_item_ids: list[str] = kwargs["stock_item_ids"]
        return {"request": {"StockItemIDs": stock_item_ids}}


class SetStockLevelBySKU(LinnworksAPIRequest):
    """Update the stock level for a product."""

    URL = "https://eu-ext.linnworks.net/api/Stock/UpdateStockLevelsBySKU"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def params(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Return request URL parameters."""
        return {"changeSource": str(kwargs["change_source"])}

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        location_id: str = kwargs["location_id"]
        changes: tuple[tuple[str, int]] = kwargs["changes"]
        stock_levels = [
            {"SKU": str(sku), "LocationID": location_id, "Level": int(level)}
            for sku, level in changes
        ]
        return {"stockLevels": stock_levels}


class AddImageToInventoryItem(LinnworksAPIRequest):
    """Adds and image to the stock item."""

    URL = "https://eu-ext.linnworks.net/api/Inventory/AddImageToInventoryItem"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        item_number: str = kwargs.get("item_number", "")
        stock_item_id: str = kwargs.get("stock_item_id", "")
        is_main: bool = kwargs["is_main"]
        image_url: str = kwargs["image_url"]
        request_data = {
            "IsMain": is_main,
            "ImageUrl": image_url,
        }
        if not item_number and not stock_item_id:
            raise ValueError("Either `stock_item_id` or `sku` must be passed.")
        if item_number:
            request_data["ItemNumber"] = item_number
        if stock_item_id:
            request_data["StockItemId"] = stock_item_id
        return {"request": request_data}
