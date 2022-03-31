"""Methods for interacting with the Linnworks inventory."""

from typing import MutableMapping

from linnapi import exceptions, models
from linnapi.request import MultiItemRequest, make_request
from linnapi.requests.inventory import (
    AddImageToInventoryItem,
    DeleteImagesFromInventoryItem,
    GetInventoryItemImages,
    GetStockItemIDsBySKU,
    GetStockLevel,
    SetStockLevelBySKU,
    UpdateImages,
)


def get_stock_item_ids_by_sku(skus: list[str]) -> MutableMapping[str, str]:
    """Return the stock item ID for a product SKU."""
    response_data = make_request(GetStockItemIDsBySKU, skus=skus)
    return {item["SKU"]: item["StockItemId"] for item in response_data["Items"]}


def get_stock_item_id_by_sku(sku: str) -> str:
    """Return the stock item ID for a product SKU."""
    stock_item_ids = get_stock_item_ids_by_sku(skus=[sku])
    try:
        return stock_item_ids[sku]
    except KeyError:
        raise exceptions.InvalidResponseError("Requested SKU not in response.")


def get_stock_level_by_stock_id(stock_item_id: str) -> models.StockLevelInfo:
    """Return stock level information for a product by stock item ID."""
    stock_level_data = make_request(GetStockLevel, stock_item_id=stock_item_id)
    return models.StockLevelInfo(stock_level_data[0])


def get_stock_level_by_sku(sku: str) -> models.StockLevelInfo:
    """Return stock level information for a product by stock item ID."""
    stock_item_id = get_stock_item_id_by_sku(sku=sku)
    stock_level_data = make_request(GetStockLevel, stock_item_id=stock_item_id)
    return models.StockLevelInfo(stock_level_data[0])


def set_stock_level(
    changes: tuple[tuple[str, int]], location_id: str, change_source: str = ""
) -> list[models.StockLevelInfo]:
    """Update the stock level for multiple products by SKU by a relative amount.

    Kwargs:
        changes: tuple(tuple(SKU, level)).
        location_id: The ID of the product's location.
    """
    updated_stock_data = make_request(
        SetStockLevelBySKU,
        location_id=location_id,
        changes=changes,
        change_source=change_source,
    )
    return [models.StockLevelInfo(_) for _ in updated_stock_data]


def add_image_to_inventory_item(
    image_url: str,
    sku: str | None = None,
    stock_item_id: str | None = None,
    is_main: bool = False,
) -> models.InventoryItemImage:
    """Add an image to a product."""
    inventory_image = make_request(
        AddImageToInventoryItem,
        item_number=sku,
        is_main=is_main,
        image_url=image_url,
        stock_item_id=stock_item_id,
    )
    return models.InventoryItemImage(inventory_image)


def get_inventory_item_images(inventory_item_id: str) -> list[models.StockItemImage]:
    """Get image information for a product."""
    response = make_request(GetInventoryItemImages, inventory_item_id=inventory_item_id)
    return [models.StockItemImage(stock_item_image) for stock_item_image in response]


class UpdateImageRequster(MultiItemRequest):
    """Requester for requesting multiple image updates."""

    request_method = UpdateImages

    def add_request(  # type: ignore[override]
        self, image_id: str, stock_item_id: str, sort_order: int, is_main: bool = False
    ) -> None:
        """
        Add an image update request.

        Kwargs:
            image_id (str): The ID (GUID) of the image to update.
            stock_item_id (str): The ID (GUID) of the product the image belongs to.
            sort_order (int): The position of the image.
            is_main (bool): Is the image the main image for the product.
        """
        kwargs = {
            "row_id": image_id,
            "stock_item_id": stock_item_id,
            "sort_order": sort_order,
            "is_main": is_main,
        }
        self._add_request(kwargs)


class DeleteImagesRequester(MultiItemRequest):
    """Requester for deleting images from inventory items."""

    request_method = DeleteImagesFromInventoryItem

    def add_request(self, stock_item_id: str, image_url: str) -> None:  # type: ignore[override]
        """
        Add a delete image request.

        Kwargs:
        image_id (str): ID (GUID) of image, passed as "pkRowId". Required.
        stock_item_id (str): The ID (GUID) of the stock item to which the image
            belongs. Requred.
        """
        kwargs = {"stock_item_id": stock_item_id, "image_url": image_url}
        self._add_request(kwargs)
