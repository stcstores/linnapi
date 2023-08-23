"""Models for Linnworks API response data."""

import datetime as dt
from typing import Any

import pytz


def parse_date_time(date_time_string: str) -> dt.datetime:
    """Return a date time string as datetime.datetime."""
    numeric_string = date_time_string.replace("Z", "")
    date, time = numeric_string.split("T")
    year, month, day = date.split("-")
    if "." in time:
        time, microsecond = time.split(".")
        microsecond = microsecond[:6]
    else:
        microsecond = "0"
    hour, minute, second = time.split(":")
    try:
        date_time = dt.datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second),
            microsecond=int(microsecond),
        )
    except ValueError:
        raise ValueError(f'Error parsing datestring "{date_time_string}".')
    date_time.replace(tzinfo=pytz.utc)
    return date_time


class StockLevelInfo:
    """Model for product stock level information."""

    def __init__(self, stock_level_data: dict[str, Any]):
        """Model for product stock level information."""
        self.raw = stock_level_data
        self.available = stock_level_data["Available"]
        self.due = stock_level_data["Due"]
        self.in_order_book = stock_level_data["InOrderBook"]
        self.in_orders = stock_level_data["InOrders"]
        self.jit = stock_level_data["JIT"]
        self.last_update_date = parse_date_time(stock_level_data["LastUpdateDate"])
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


class ProcessedOrder:
    """Model for processed orders."""

    def __init__(self, processed_order: dict[str, Any]):
        """Model for processed orders."""
        self.raw = processed_order
        self.order_guid: str = processed_order["pkOrderID"]
        self.received_date: dt.datetime = parse_date_time(
            processed_order["dReceivedDate"]
        )
        self.processed_at: dt.datetime = parse_date_time(
            processed_order["dProcessedOn"]
        )
        self.time_diff = float(processed_order["timeDiff"])
        self.postage_cost = float(processed_order["fPostageCost"])
        self.total_charge = float(processed_order["fTotalCharge"])
        self.postage_cost_ex_tax = float(processed_order["PostageCostExTax"])
        self.subtotal = float(processed_order["Subtotal"])
        self.tax = float(processed_order["fTax"])
        self.total_discount = float(processed_order["TotalDiscount"])
        self.profit_margin = float(processed_order["ProfitMargin"])
        self.country_tax_rate = float(processed_order["CountryTaxRate"])
        self.order_id = str(processed_order["nOrderId"])
        self.status_number = int(processed_order["nStatus"])
        self.currency: str = processed_order["cCurrency"]
        self.tracking_number: str = processed_order["PostalTrackingNumber"]
        self.country: str = processed_order["cCountry"]
        self.source: str = processed_order["Source"]
        self.subsource: str = processed_order["SubSource"]
        self.postal_service: str = processed_order["PostalServiceName"]
        self.reference_number: str = processed_order["ReferenceNum"]
        self.secondary_reference: str = processed_order["SecondaryReference"]
        self.external_reference: str = processed_order["ExternalReference"]
        self.address_1: str = processed_order["Address1"]
        self.address_2: str = processed_order["Address2"]
        self.address_3: str = processed_order["Address3"]
        self.town: str = processed_order["Town"]
        self.region: str = processed_order["Region"]
        self.buyer_phone_number: str = processed_order["BuyerPhoneNumber"]
        self.company: str = processed_order["Company"]
        self.channel_buyer_name: str = processed_order["ChannelBuyerName"]
        self.account_name: str = processed_order["AccountName"]
        self.customer_full_name: str = processed_order["cFullName"]
        self.customer_email_address: str = processed_order["cEmailAddress"]
        self.customer_post_code: str = processed_order["cPostCode"]
        self.paid_at: dt.datetime = parse_date_time(processed_order["dPaidOn"])
        self.cancelled_at: dt.datetime | None = parse_date_time(
            processed_order["dCancelledOn"]
        )
        if self.cancelled_at.year == 1:
            self.cancelled_at = None
        self.item_weight = int(processed_order["ItemWeight"])
        self.total_weight = int(processed_order["TotalWeight"])
        self.hold_or_cancel: bool = processed_order["HoldOrCancel"]
        self.is_resend: bool = processed_order["IsResend"]
        self.is_exchange: bool = processed_order["IsExchange"]
        self.tax_id: str = processed_order["TaxId"]
        self.fulfilment_location_name: str = processed_order["FulfilmentLocationName"]


class OrderAuditTrailEntry:
    """Model for order audit trail entries."""

    def __init__(self, audit_trail_entry: dict[str, Any]):
        """Model for order audit trail entries."""
        self.raw = audit_trail_entry
        self.history_id: int = audit_trail_entry["sid_history"]
        self.order_guid: str = audit_trail_entry["fkOrderId"]
        self.history_note: str = audit_trail_entry["HistoryNote"]
        self.timestamp: dt.datetime = parse_date_time(audit_trail_entry["DateStamp"])
        self.tag: str = audit_trail_entry["Tag"]
        self.updated_by = audit_trail_entry["UpdatedBy"]
        self.audit_type = audit_trail_entry["fkOrderHistoryTypeId"]
        self.type_description: str = audit_trail_entry["TypeDescription"]


class StockItemHistoryRecord:
    """Model for stock item history records."""

    def __init__(self, stock_item_record: dict[str, Any]):
        """Model for stock item history records."""
        self.raw = stock_item_record
        self.timestamp = parse_date_time(stock_item_record["Date"])
        self.stock_level = stock_item_record["Level"]
        self.text = stock_item_record["Note"]
        self.relative_change = stock_item_record["ChangeQty"]
        self.stock_item_id = stock_item_record["StockItemId"]


class ChannelLinkedItem:
    """Model for channel linked items."""

    def __init__(self, channel_linked_item: dict[str, Any]):
        """Model for channel linked items."""
        self.raw = channel_linked_item
        self.channel_sku_id = channel_linked_item["ChannelSKURowId"]
        self.sku = channel_linked_item["SKU"]
        self.source = channel_linked_item["Source"]
        self.sub_source = channel_linked_item["SubSource"]
        self.update_status = channel_linked_item["UpdateStatus"]
        self.channel_reference_id = channel_linked_item["ChannelReferenceId"]
        self.last_update = parse_date_time(channel_linked_item["LastUpdate"])
        self.max_listed_quantity = channel_linked_item["MaxListedQuantity"]
        self.end_when_stock = channel_linked_item["EndWhenStock"]
        self.submitted_quantity = channel_linked_item["SubmittedQuantity"]
        self.listed_quantity = channel_linked_item["ListedQuantity"]
        self.stock_percentage = channel_linked_item["StockPercentage"]
        self.ignore_sync = channel_linked_item["IgnoreSync"]
        self.is_multi_location = channel_linked_item["IsMultiLocation"]
        self.stock_item_id = channel_linked_item["StockItemId"]
