"""Models for Linnworks API response data."""

import datetime as dt
from typing import Any

import pytz


class StockLevelInfo:
    """Model for product stock level information."""

    def __init__(self, stock_level_data: dict[str, Any]):
        """Model for product stock level information."""
        self.raw = stock_level_data
        self.auto_adjust = stock_level_data["AutoAdjust"]
        self.available = stock_level_data["Available"]
        self.due = stock_level_data["Due"]
        self.in_order_book = stock_level_data["InOrderBook"]
        self.in_orders = stock_level_data["InOrders"]
        self.jit = stock_level_data["JIT"]
        self.last_update_date = self.parse_date_time(stock_level_data["LastUpdateDate"])
        self.last_update_operation = stock_level_data["LastUpdateOperation"]

        self.location_is_fulfillment_center = stock_level_data["Location"][
            "IsFulfillmentCenter"
        ]
        self.location_is_warehouse_managed = stock_level_data["Location"].get(
            "IsWarehouseManaged"
        )
        self.location_name = stock_level_data["Location"]["LocationName"]
        self.location_id = stock_level_data["Location"]["StockLocationId"]
        self.location_int_id = stock_level_data["Location"]["StockLocationIntId"]

        self.minimum_level = stock_level_data["MinimumLevel"]
        self.pending_update = stock_level_data["PendingUpdate"]
        self.sku = stock_level_data["SKU"]
        self.stock_item_id = stock_level_data["StockItemId"]
        self.stock_item_int_id = stock_level_data["StockItemIntId"]
        self.stock_item_purchase_price = stock_level_data["StockItemPurchasePrice"]
        self.stock_level = stock_level_data["StockLevel"]
        self.stock_value = stock_level_data["StockValue"]
        self.unit_cost = stock_level_data["UnitCost"]
        self.row_id = stock_level_data["rowid"]

    @staticmethod
    def parse_date_time(date_time_string: str) -> dt.datetime:
        """Return a date time string as datetime.datetime."""
        date_time_string = date_time_string.replace("Z", "")
        date, time = date_time_string.split("T")
        year, month, day = date.split("-")
        if "." in time:
            time, microsecond = time.split(".")
        else:
            microsecond = "0"
        hour, minute, second = time.split(":")
        date_time = dt.datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second),
            microsecond=int(microsecond),
        )
        date_time.replace(tzinfo=pytz.utc)
        return date_time


class InventoryItemImage:
    """Model for inventory image information."""

    def __init__(self, inventory_image: dict[str, Any]):
        """Model for inventory image information."""
        self.raw = inventory_image
        self.stock_item_id: str = inventory_image["StockItemId"]
        self.image_id: str = inventory_image["ImageId"]
        self.image_url: str = inventory_image["ImageUrl"]
        self.image_thumbnail_url: str = inventory_image["ImageThumbnailUrl"]


class StockItemImage:
    """Model for stock item image information."""

    def __init__(self, stock_item_image: dict[str, Any]):
        """Model for stock item image information."""
        self.raw = stock_item_image
        self.source: str = stock_item_image["Source"]
        self.full_source: str = stock_item_image["FullSource"]
        self.checksum_value: str = stock_item_image["CheckSumValue"]
        self.image_id: str = stock_item_image["pkRowId"]
        self.is_main: bool = stock_item_image["IsMain"]
        self.sort_order: int = stock_item_image["SortOrder"]
        self.stock_item_id: str = stock_item_image["StockItemId"]
        self.stock_item_int_id: int = stock_item_image["StockItemIntId"]
