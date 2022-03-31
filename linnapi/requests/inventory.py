"""Inventory requests."""

from collections import defaultdict
from typing import Any, MutableMapping

import requests

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
    """
    Adds an image to a stock item.

    Either `item_number` or `stock_item_id` must be passed.

    Kwargs:
        image_url (str): The URL of the image to be added.
        item_number (str): The SKU of the product to add the image to.
        stock_item_id (str): The ID (GUID) of the product to add the image to.
        is_main (bool): Is the image the main image for the product.
    """

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


class UpdateImages(LinnworksAPIRequest):
    """
    Update properties on images.

    Kwargs:
        row_id (str): ID (GUID) of image, passed as "pkRowId". Required.
        stock_item_id (str): The ID (GUID) of the stock item to which the image
            belongs. Requred.
        is_main (bool): Set weather the image is the main image or not, passed as "IsMain".
        sort_order (int): The position of the image, passed as "SortOrder".
    """

    URL = "https://eu-ext.linnworks.net/api/Inventory/UpdateImages"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def item_json(cls, **kwargs: Any) -> dict[str, Any]:
        """Return request data for a single image."""
        row_id = kwargs.get("row_id")
        is_main = kwargs.get("is_main")
        sort_order = kwargs.get("sort_order")
        checksum_value = kwargs.get("checksum_value")
        raw_checksum = kwargs.get("raw_checksum")
        stock_item_id = kwargs.get("stock_item_id")
        stock_item_int_id = kwargs.get("stock_item_id_int")
        image_data = {
            "pkRowId": row_id,
            "IsMain": is_main,
            "SortOrder": sort_order,
            "ChecksumValue": checksum_value,
            "RawChecksum": raw_checksum,
            "StockItemId": stock_item_id,
            "StockItemIntId": stock_item_int_id,
        }
        return {key: value for key, value in image_data.items() if value is not None}

    @classmethod
    def multi_json(
        cls, requests: list[MutableMapping[Any, Any]]
    ) -> dict[str, Any] | list[Any]:
        """Return request JSON with multiple updates."""
        return {"images": [cls.item_json(**request) for request in requests]}

    @classmethod
    def parse_response(
        cls, response: requests.models.Response, *args: Any, **kwargs: Any
    ) -> str:
        """Parse the request response."""
        return response.text


class GetInventoryItemImages(LinnworksAPIRequest):
    """
    Use this call to Get inventory item images.

    Args:
        inventory_item_id (str): The ID (GUID) of the stock item to retrive images for,
            passed as "InventoryItemId".
    """

    URL = "https://eu-ext.linnworks.net/api/Inventory/GetInventoryItemImages"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def json(cls, *args: Any, **kwargs: Any) -> dict[str, Any] | list[Any]:
        """Return request JSON post data."""
        inventory_item_id = kwargs.get("inventory_item_id")
        return {"inventoryItemId": inventory_item_id}


class DeleteImagesFromInventoryItem(LinnworksAPIRequest):
    """
    Remove an image from an inventory item.

    Kwargs:
        image_id (str): ID (GUID) of image, passed as "pkRowId". Required.
        stock_item_id (str): The ID (GUID) of the stock item to which the image
            belongs. Requred.
    """

    URL = "https://eu-ext.linnworks.net/api/Inventory/DeleteImagesFromInventoryItem"
    METHOD = LinnworksAPIRequest.POST

    @classmethod
    def item_json(cls, **kwargs: Any) -> dict[str, Any]:
        """Return request data for a single image."""
        stock_item_id = kwargs["stock_item_id"]
        image_url = kwargs["image_url"]
        return {stock_item_id: [image_url]}

    @classmethod
    def multi_json(
        cls, requests: list[MutableMapping[Any, Any]]
    ) -> dict[str, Any] | list[Any]:
        """Return request JSON with multiple updates."""
        stock_items = defaultdict(list)
        for request in requests:
            for key, images in cls.item_json(**request).items():
                stock_items[key].extend(images)
        return {"inventoryItemImages": dict(stock_items)}

    @classmethod
    def parse_response(
        cls, response: requests.models.Response, *args: Any, **kwargs: Any
    ) -> str:
        """Parse the request response."""
        return response.text
