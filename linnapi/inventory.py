"""Methods for interacting with the Linnworks inventory."""

from typing import MutableMapping

from linnapi import exceptions, models
from linnapi.request import MultiItemRequest, make_request
from linnapi.requests.inventory import (
    AddImageToInventoryItem,
    BatchGetInventoryItemChannelSKUs,
    DeleteImagesFromInventoryItem,
    DeleteInventoryItemChannelSKUs,
    GetInventoryItemImages,
    GetItemChangesHistory,
    GetStockItemIDsBySKU,
    GetStockLevel,
    GetStockLevelBatch,
    SetStockLevelBySKU,
    UpdateImages,
)


def get_stock_item_ids_by_sku(*skus: str) -> MutableMapping[str, str]:
    """Return the stock item ID for a product SKU."""
    response = make_request(GetStockItemIDsBySKU, skus=skus)
    try:
        return {item["SKU"]: item["StockItemId"] for item in response["Items"]}
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")


def get_stock_item_id_by_sku(sku: str) -> str:
    """Return the stock item ID for a product SKU."""
    stock_item_ids = get_stock_item_ids_by_sku(sku)
    try:
        return stock_item_ids[sku]
    except KeyError:
        raise exceptions.InvalidResponseError("Requested SKU not in response.")


def get_stock_level_by_stock_id(stock_item_id: str) -> models.StockLevelInfo:
    """Return stock level information for a product by stock item ID."""
    response = make_request(GetStockLevel, stock_item_id=stock_item_id)
    try:
        return models.StockLevelInfo(response[0])
    except (KeyError, IndexError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")


def get_stock_level_by_sku(sku: str) -> models.StockLevelInfo:
    """Return stock level information for a product by stock item ID."""
    stock_item_id = get_stock_item_id_by_sku(sku=sku)
    response = make_request(GetStockLevel, stock_item_id=stock_item_id)
    try:
        stock_level_info = models.StockLevelInfo(response[0])
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return stock_level_info


def get_stock_levels_by_skus(*skus: str) -> dict[str, models.StockLevelInfo]:
    """Return stock level information for multliple SKUs."""
    stock_item_id_lookup = get_stock_item_ids_by_sku(*skus)
    stock_item_ids = list(stock_item_id_lookup.values())
    response = make_request(GetStockLevelBatch, stock_item_ids=stock_item_ids)
    stock_levels = {}
    try:
        for response_item in response:
            for stock_level in response_item["StockItemLevels"]:
                stock_level_info = models.StockLevelInfo(stock_level)
                stock_levels[stock_level_info.sku] = stock_level_info
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    if set(skus) != set(stock_levels.keys()):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    return stock_levels


def set_stock_level(
    changes: tuple[tuple[str, int]], location_id: str, change_source: str = ""
) -> list[models.StockLevelInfo]:
    """Update the stock level for multiple products by SKU by a relative amount.

    Kwargs:
        changes: tuple(tuple(SKU, level)).
        location_id: The ID of the product's location.
    """
    response = make_request(
        SetStockLevelBySKU,
        location_id=location_id,
        changes=changes,
        change_source=change_source,
    )
    try:
        stock_level_info = [models.StockLevelInfo(_) for _ in response]
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return stock_level_info


def add_image_to_inventory_item(
    image_url: str,
    sku: str | None = None,
    stock_item_id: str | None = None,
    is_main: bool = False,
) -> models.InventoryItemImage:
    """Add an image to a product."""
    response = make_request(
        AddImageToInventoryItem,
        item_number=sku,
        is_main=is_main,
        image_url=image_url,
        stock_item_id=stock_item_id,
    )
    try:
        inventory_item_image = models.InventoryItemImage(response)
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return inventory_item_image


def get_inventory_item_images(inventory_item_id: str) -> list[models.StockItemImage]:
    """Get image information for a product."""
    response = make_request(GetInventoryItemImages, inventory_item_id=inventory_item_id)
    try:
        stock_item_images = [
            models.StockItemImage(stock_item_image) for stock_item_image in response
        ]
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return stock_item_images


def get_stock_level_history_by_stock_item_id(
    stock_item_id: str,
    location_id: str,
    entries_per_page: int = 500,
    page_number: int = 1,
) -> list[models.StockItemHistoryRecord]:
    """Return a history of stock level changes for a stock item ID."""
    response = make_request(
        GetItemChangesHistory,
        stock_item_id=stock_item_id,
        location_id=location_id,
        entries_per_page=entries_per_page,
        page_number=page_number,
    )
    try:
        records = [models.StockItemHistoryRecord(_) for _ in response["Data"]]
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    else:
        return sorted(records, key=lambda x: x.timestamp, reverse=True)


def get_stock_level_history_by_sku(
    sku: str,
    location_id: str,
) -> list[models.StockItemHistoryRecord]:
    """Return a history of stock level changes for a product SKU."""
    stock_item_id = get_stock_item_id_by_sku(sku)
    return get_stock_level_history_by_stock_item_id(
        stock_item_id=stock_item_id, location_id=location_id
    )


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


def get_item_channel_skus(
    *stock_item_ids: str,
) -> dict[str, list[models.ChannelLinkedItem]]:
    """Return details of channel listings linked to stock items."""
    response = make_request(
        BatchGetInventoryItemChannelSKUs, stock_item_ids=stock_item_ids
    )
    channel_skus = {}
    try:
        for stock_item in response:
            item_channel_skus = [
                models.ChannelLinkedItem(item) for item in stock_item["ChannelSkus"]
            ]
            channel_skus[stock_item["StockItemId"]] = item_channel_skus
    except (KeyError, IndexError, TypeError):
        raise exceptions.InvalidResponseError(f"Invalid Response: {response}")
    return channel_skus


def get_channel_skus_by_skus(*skus: str) -> dict[str, list[models.ChannelLinkedItem]]:
    """Return details of channel listings linked to stock items by SKU."""
    sku_stock_item_ids = get_stock_item_ids_by_sku(*skus)
    stock_item_ids = list(sku_stock_item_ids.values())
    channel_items = get_item_channel_skus(*stock_item_ids)
    return {
        sku: channel_items[stock_item_id]
        for sku, stock_item_id in sku_stock_item_ids.items()
    }


def delete_channel_sku_links(*inventory_item_channel_sku_ids: list[str]) -> None:
    """Delete a channel link by channel link ID."""
    response = make_request(
        DeleteInventoryItemChannelSKUs,
        inventory_item_channel_sku_ids=inventory_item_channel_sku_ids,
    )
    if response is False:
        raise exceptions.InvalidResponseError(
            "Delete channel item SKU link returned non-success response."
        )
