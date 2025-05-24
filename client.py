"""HTTP client for Yango Tech B2B API."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx
from httpx import AsyncClient, Response

from models import AuthConfig, Order, PaginatedResponse, Product, Stock

logger = logging.getLogger(__name__)


class YangoTechAPIError(Exception):
    """Exception for Yango Tech API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class YangoTechClient:
    """Client for Yango Tech B2B API."""

    def __init__(self, config: AuthConfig):
        """Initialize client."""
        self.config = config
        self.client: Optional[AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def connect(self) -> None:
        """Establish connection to API."""
        if self.client is None:
            self.client = AsyncClient(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
                headers={
                    "Authorization": f"OAuth {self.config.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "MCP-Server-YangoTech/0.1.0"
                }
            )

    async def disconnect(self) -> None:
        """Close connection to API."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute HTTP request to API."""
        if not self.client:
            await self.connect()

        url = endpoint if endpoint.startswith("http") else f"/b2b/v1{endpoint}"

        for attempt in range(self.config.max_retries):
            try:
                logger.debug(f"Making {method} request to {url}, attempt {attempt + 1}")

                response: Response = await self.client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise YangoTechAPIError(
                        "Authentication error. Check API key.",
                        status_code=response.status_code
                    )
                elif response.status_code == 404:
                    raise YangoTechAPIError(
                        "Resource not found",
                        status_code=response.status_code
                    )
                elif response.status_code >= 500:
                    if attempt == self.config.max_retries - 1:
                        raise YangoTechAPIError(
                            f"Server error: {response.status_code}",
                            status_code=response.status_code
                        )
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except Exception:
                        pass

                    raise YangoTechAPIError(
                        f"API error: {response.status_code} - {error_data.get('message', 'Unknown error')}",
                        status_code=response.status_code,
                        response_data=error_data
                    )

            except httpx.RequestError as e:
                if attempt == self.config.max_retries - 1:
                    raise YangoTechAPIError(f"Connection error: {str(e)}")
                await asyncio.sleep(2 ** attempt)

        raise YangoTechAPIError("Maximum retry attempts exceeded")

    # Order management methods

    async def get_order_details(self, order_id: str) -> Order:
        """Get order details by order number."""
        data = await self._make_request("POST", "/orders/get", {"order_id": order_id})
        return Order(**data)

    async def get_order_status(self, order_id: str) -> str:
        """Get order status by order number."""
        data = await self._make_request("POST", "/orders/state", {"orders": [order_id]})
        if data.get("query_results") and len(data["query_results"]) > 0:
            result = data["query_results"][0]
            if result.get("query_result") == "success":
                return result.get("state", "unknown")
            else:
                raise YangoTechAPIError(f"Error getting order status: {result.get('query_result')}")
        raise YangoTechAPIError("Failed to get order status")

    # get_order_tracking method removed - API endpoint not confirmed in documentation

    # Product management methods

    async def get_all_products(self) -> List[Product]:
        """Get all products with cursor-based reading."""
        products = []
        cursor = None

        while True:
            body = {"cursor": cursor, "limit": 100}
            data = await self._make_request("POST", "/products/query", body)

            batch_products = [Product(**item) for item in data.get("products", [])]

            # Exit if no objects returned OR no cursor
            if not batch_products:
                logger.info("No more products returned from API")
                break

            products.extend(batch_products)

            cursor = data.get("cursor")
            if not cursor:
                logger.info("No more cursor returned from API")
                break

        logger.info(f"Loaded {len(products)} products")
        return products

    async def get_products_batch(self, cursor: Optional[str] = None, limit: int = 100) -> PaginatedResponse:
        """Get product batch."""
        body = {"cursor": cursor, "limit": limit}
        data = await self._make_request("POST", "/products/query", body)

        products_data = data.get("products", [])
        next_cursor = data.get("cursor")

        # has_more is True if we have cursor AND got products
        has_more = bool(next_cursor and products_data)

        return PaginatedResponse(
            data=[Product(**item) for item in products_data],
            next_cursor=next_cursor,
            has_more=has_more,
            total_count=None  # API doesn't return total_count
        )

    # Price management methods removed - API doesn't support them

    # Stock management methods

    async def get_all_stocks(self) -> List[Stock]:
        """Get all product stocks with cursor-based reading."""
        stocks = []
        cursor = None

        while True:
            body = {"cursor": cursor, "limit": 100}
            data = await self._make_request("POST", "/stocks/query", body)

            batch_stocks = [Stock(**item) for item in data.get("stocks", [])]

            # Exit if no objects returned OR no cursor
            if not batch_stocks:
                logger.info("No more stocks returned from API")
                break

            stocks.extend(batch_stocks)

            cursor = data.get("cursor")
            if not cursor:
                logger.info("No more cursor returned from API")
                break

        logger.info(f"Loaded {len(stocks)} stocks")
        return stocks

    async def get_stocks_batch(self, cursor: Optional[str] = None, limit: int = 100) -> PaginatedResponse:
        """Get stock batch."""
        body = {"cursor": cursor, "limit": limit}
        data = await self._make_request("POST", "/stocks/query", body)

        stocks_data = data.get("stocks", [])
        next_cursor = data.get("cursor")

        # has_more is True if we have cursor AND got stocks
        has_more = bool(next_cursor and stocks_data)

        return PaginatedResponse(
            data=[Stock(**item) for item in stocks_data],
            next_cursor=next_cursor,
            has_more=has_more,
            total_count=None
        )
