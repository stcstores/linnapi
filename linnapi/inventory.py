"""Methods for interacting with the Linnworks inventory."""

from typing import MutableMapping

from linnapi import exceptions, models
from linnapi.request import make_request
from linnapi.requests.inventory import (
    GetStockItemIDsBySKU,
    GetStockLevel,
    SetStockLevelBySKU,
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
