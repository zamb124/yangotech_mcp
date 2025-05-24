"""Data models for Yango Tech B2B API."""

import os
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order statuses in Yango Tech."""
    CREATED = "created"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class ProductCategory(str, Enum):
    """Product categories."""
    FOOD = "food"
    ELECTRONICS = "electronics"
    HOUSEHOLD = "household"
    CLOTHING = "clothing"
    BEAUTY = "beauty"
    OTHER = "other"


class Store(BaseModel):
    """Store model."""
    id: str = Field(description="Unique store identifier")
    name: str = Field(description="Store name")
    address: str = Field(description="Store address")
    city: str = Field(description="City")
    phone: Optional[str] = Field(None, description="Store phone number")
    email: Optional[str] = Field(None, description="Store email")
    working_hours: Optional[str] = Field(None, description="Working hours")
    is_active: bool = Field(True, description="Whether store is active")


class Product(BaseModel):
    """Product model according to real API."""
    product_id: str = Field(description="Unique product identifier")
    master_category: str = Field(description="Main product category")
    status: str = Field(description="Product status (active/inactive)")
    is_meta: bool = Field(description="Whether product is meta-product")
    custom_attributes: Dict[str, Any] = Field(description="Custom product attributes")

    # Convenience methods for getting data from custom_attributes
    @property
    def name(self) -> Optional[str]:
        """Get product name."""
        short_name = self.custom_attributes.get("shortNameLoc", {})
        if isinstance(short_name, dict):
            return short_name.get("ru_RU") or short_name.get("uz_UZ")
        return None

    @property
    def long_name(self) -> Optional[str]:
        """Get full product name."""
        long_name = self.custom_attributes.get("longName", {})
        if isinstance(long_name, dict):
            return long_name.get("ru_RU") or long_name.get("uz_UZ")
        return None

    @property
    def barcode(self) -> Optional[List[str]]:
        """Get product barcodes."""
        return self.custom_attributes.get("barcode")


class Price(BaseModel):
    """Product price model."""
    product_id: str = Field(description="Product identifier")
    store_id: str = Field(description="Store identifier")
    price: Decimal = Field(description="Product price")
    currency: str = Field("RUB", description="Currency")
    updated_at: datetime = Field(description="Last price update date")


class Stock(BaseModel):
    """Product stock model according to real API."""
    store_id: str = Field(description="Store identifier")
    product_id: str = Field(description="Product identifier")
    quantity: int = Field(description="Product quantity in stock")
    shelf_type: str = Field(description="Shelf/warehouse type (store, etc.)")


class Position(BaseModel):
    """Location coordinates."""
    lat: float = Field(description="Latitude")
    lon: float = Field(description="Longitude")


class Address(BaseModel):
    """Address."""
    country: str = Field(description="Country")
    city: str = Field(description="City")
    street: str = Field(description="Street")
    house: str = Field(description="House number")


class DeliveryAddress(BaseModel):
    """Delivery address according to real API."""
    position: Position = Field(description="Coordinates")
    place_id: str = Field(description="Place identifier")
    address: Address = Field(description="Address")


class CartItem(BaseModel):
    """Cart item."""
    product_id: str = Field(description="Product identifier")
    quantity: int = Field(description="Quantity")
    price: str = Field(description="Price (string)")
    price_per_quantity: int = Field(description="Price per quantity")


class Cart(BaseModel):
    """Order cart."""
    total_price: str = Field(description="Total cost (string)")
    items: List[CartItem] = Field(description="Items in cart")


class DeliveryProperties(BaseModel):
    """Delivery properties."""
    type: str = Field(description="Delivery type (pickup, delivery)")


class Customer(BaseModel):
    """Customer."""
    id: str = Field(description="Customer identifier")
    name: str = Field(description="Customer name")
    phone: str = Field(description="Customer phone")
    email: Optional[str] = Field(None, description="Customer email")


class Order(BaseModel):
    """Order model according to real API."""
    create_time: str = Field(description="Order creation time")
    store_id: str = Field(description="Store identifier")
    client_phone_number: str = Field(description="Client phone number")
    payment_type: str = Field(description="Payment type (cash, card)")
    payment_status: str = Field(description="Payment status (paid, pending)")
    delivery_address: DeliveryAddress = Field(description="Delivery address")
    use_external_logistics: bool = Field(description="Use external logistics")
    cart: Cart = Field(description="Order cart")
    delivery_properties: DeliveryProperties = Field(description="Delivery properties")
    human_order_id: str = Field(description="Human-readable order ID")
    trace_id: Optional[str] = Field(None, description="Trace ID")

    # Convenience properties for compatibility
    @property
    def id(self) -> str:
        """Get order ID."""
        return self.human_order_id

    @property
    def total_amount(self) -> str:
        """Get total amount."""
        return self.cart.total_price


class TrackingEvent(BaseModel):
    """Order tracking event."""
    timestamp: datetime = Field(description="Event time")
    status: OrderStatus = Field(description="Status")
    location: Optional[str] = Field(None, description="Location")
    description: str = Field(description="Event description")
    courier_id: Optional[str] = Field(None, description="Courier identifier")


class OrderTracking(BaseModel):
    """Order tracking."""
    order_id: str = Field(description="Order number")
    current_status: OrderStatus = Field(description="Current status")
    events: List[TrackingEvent] = Field(description="Event history")
    estimated_delivery_time: Optional[datetime] = Field(None, description="Estimated delivery time")


class APIResponse(BaseModel):
    """Base API response model."""
    success: bool = Field(description="Operation success")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message")
    pagination: Optional[Dict[str, Any]] = Field(None, description="Pagination information")


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    data: List[Any] = Field(description="Data")
    next_cursor: Optional[str] = Field(None, description="Cursor for next page")
    has_more: bool = Field(False, description="Whether there is more data")
    total_count: Optional[int] = Field(None, description="Total record count")


class AuthConfig(BaseModel):
    """Authentication configuration."""
    api_key: str = Field(description="API key")
    base_url: str = Field("https://api.retailtech.yango.com", description="Base API URL")
    timeout: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retry attempts")

    @classmethod
    def from_env(cls) -> "AuthConfig":
        """Create configuration from environment variables."""
        return cls(
            api_key=os.getenv("YANGO_TECH_API_KEY", ""),
            base_url=os.getenv("YANGO_TECH_BASE_URL", "https://api.tst.eu.cloudretail.tech"),
            timeout=int(os.getenv("YANGO_TECH_TIMEOUT", "30")),
            max_retries=int(os.getenv("YANGO_TECH_MAX_RETRIES", "3"))
        )
