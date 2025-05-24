#!/usr/bin/env python3
"""MCP server for Yango Tech B2B API integration based on FastMCP."""

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP

from client import YangoTechAPIError, YangoTechClient
from models import AuthConfig, Product

# Load environment variables
load_dotenv()

# Create FastMCP server
mcp = FastMCP("Yango Tech B2B API")

# Global variables
_client: Optional[YangoTechClient] = None
_products_cache: Dict[str, Product] = {}  # product_id -> Product
_cache_loaded: bool = False


def get_client() -> YangoTechClient:
    """Get Yango Tech API client."""
    global _client

    if _client is None:
        api_key = os.getenv("YANGO_TECH_API_KEY")
        if not api_key:
            raise ValueError("YANGO_TECH_API_KEY environment variable is required")

        base_url = os.getenv("YANGO_TECH_BASE_URL", "https://api.retailtech.yango.com")

        config = AuthConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=int(os.getenv("YANGO_TECH_TIMEOUT", "30")),
            max_retries=int(os.getenv("YANGO_TECH_MAX_RETRIES", "3"))
        )

        _client = YangoTechClient(config)

    return _client


async def ensure_products_cache() -> None:
    """Ensure products cache is loaded."""
    global _products_cache, _cache_loaded

    if _cache_loaded:
        return

    print("📦 Loading products cache...")
    client = get_client()
    async with client:
        products = await client.get_all_products()
        # Create dict for fast lookup by product_id
        _products_cache = {product.product_id: product for product in products}
        _cache_loaded = True
    print(f"✅ Products cache loaded: {len(_products_cache)} products")


def get_product_name(product_id: str, language: str = "en_EN") -> str:
    """Get product name from cache by product_id."""
    if not _cache_loaded or product_id not in _products_cache:
        return product_id  # Return product_id if not found

    product = _products_cache[product_id]

    # Try shortNameLoc first
    short_name = product.custom_attributes.get("shortNameLoc", {})
    if isinstance(short_name, dict):
        # Try requested language first
        if language in short_name and short_name[language]:
            return short_name[language]
        
        # If requested language not found, try any available language
        for lang_code, name in short_name.items():
            if name:  # Return first non-empty name found
                return name

    # Try longName if shortNameLoc not found
    long_name = product.custom_attributes.get("longName", {})
    if isinstance(long_name, dict):
        # Try requested language first
        if language in long_name and long_name[language]:
            return long_name[language]
            
        # If requested language not found, try any available language
        for lang_code, name in long_name.items():
            if name:  # Return first non-empty name found
                return name

    return product_id  # Fallback to product_id


def enrich_order_with_product_names(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich order data with product names."""
    if not isinstance(order_data, dict):
        return order_data

    # Make a copy to avoid modifying original
    enriched_data = order_data.copy()

    # Check for cart items
    if "cart" in enriched_data and isinstance(enriched_data["cart"], dict):
        cart = enriched_data["cart"]
        if "items" in cart and isinstance(cart["items"], list):
            for item in cart["items"]:
                if isinstance(item, dict) and "product_id" in item:
                    product_id = item["product_id"]
                    product_name = get_product_name(product_id)
                    item["product_name"] = product_name

    return enriched_data


def enrich_stock_with_product_name(stock_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich single stock record with product name."""
    if not isinstance(stock_data, dict):
        return stock_data

    enriched_data = stock_data.copy()

    if "product_id" in enriched_data:
        product_id = enriched_data["product_id"]
        product_name = get_product_name(product_id)
        enriched_data["product_name"] = product_name

    return enriched_data


@mcp.tool()
async def get_order_details(order_id: str) -> str:
    """
    Get detailed information about a Yango Tech order by number.

    Use for queries like 'show order', 'order details', 'order information',
    'full order information'. Supports order numbers in format 240920-728268.

    Args:
        order_id: Yango Tech order number (e.g.: 240920-728268)

    Returns:
        Detailed order information with product names
    """
    try:
        # Ensure products cache is loaded for product name enrichment
        await ensure_products_cache()

        client = get_client()
        async with client:
            order = await client.get_order_details(order_id)
            enriched_order = enrich_order_with_product_names(order.model_dump())
            return f"Order details {order_id}:\n{json.dumps(enriched_order, ensure_ascii=False, indent=2, default=str)}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def get_order_status(order_id: str) -> str:
    """
    Get current status of a Yango Tech order.

    Use for queries like 'order status', 'order state', 'where is order',
    'what about order', 'check order'. Calls API endpoint b2b/v1/orders/state.

    Args:
        order_id: Yango Tech order number (e.g.: 240920-728268)

    Returns:
        Order status
    """
    try:
        client = get_client()
        async with client:
            status = await client.get_order_status(order_id)
            return f"Order status {order_id}: {status}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def get_all_products() -> str:
    """
    Get complete Yango Tech product catalog.

    Use for queries like 'all products', 'entire catalog', 'list all products',
    'show products'. Uses cached data for fast access.

    Returns:
        List of all products with names
    """
    try:
        # Load cache and return products from cache
        await ensure_products_cache()

        products = list(_products_cache.values())
        # Format products with readable names
        formatted_products = []
        for product in products:
            product_data = product.model_dump()
            product_data["display_name"] = get_product_name(product.product_id)
            formatted_products.append(product_data)

        return f"Retrieved {len(products)} products:\n{json.dumps(formatted_products, ensure_ascii=False, indent=2, default=str)}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def get_products_batch(cursor: Optional[str] = None, limit: int = 100) -> str:
    """
    Get Yango Tech products with pagination.

    Use for queries like 'show N products', 'first products', 'products by pages'.
    Uses cached data for fast access.

    Args:
        cursor: Starting index for pagination (string number)
        limit: Number of products to retrieve (default 100, maximum 1000)

    Returns:
        Product batch with pagination information and names
    """
    try:
        # Load cache first
        await ensure_products_cache()

        # Convert cursor to index - handle None and string cursors properly
        start_index = 0
        if cursor is not None:
            try:
                start_index = int(cursor)
            except (ValueError, TypeError):
                start_index = 0  # Fallback to beginning if cursor is invalid

        # Get products from cache
        all_products = list(_products_cache.values())
        end_index = start_index + limit
        products_slice = all_products[start_index:end_index]

        # Format with display names
        formatted_products = []
        for product in products_slice:
            product_data = product.model_dump()
            product_data["display_name"] = get_product_name(product.product_id)
            formatted_products.append(product_data)

        # Create pagination info - next_cursor is None when no more data
        next_cursor = str(end_index) if end_index < len(all_products) else None

        result = {
            "products": formatted_products,
            "pagination": {
                "current_cursor": cursor,
                "next_cursor": next_cursor,
                "has_more": end_index < len(all_products),
                "total_count": len(all_products),
                "showing": len(formatted_products)
            }
        }

        return f"Product batch (limit: {limit}, retrieved: {len(formatted_products)}):\n{json.dumps(result, ensure_ascii=False, indent=2, default=str)}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def get_all_stocks() -> str:
    """
    Get all Yango Tech product stocks in warehouses.

    Use for queries like 'all stocks', 'what is in warehouse', 'product availability',
    'warehouse stocks'. Shows stock info with product names.

    Returns:
        List of all warehouse stocks with product names
    """
    try:
        # Ensure products cache is loaded for product name enrichment
        await ensure_products_cache()

        client = get_client()
        async with client:
            stocks = await client.get_all_stocks()
        enriched_stocks = [enrich_stock_with_product_name(s.model_dump()) for s in stocks]
        return f"Retrieved {len(stocks)} stocks:\n{json.dumps(enriched_stocks, ensure_ascii=False, indent=2, default=str)}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def get_stocks_batch(cursor: Optional[str] = None, limit: int = 100) -> str:
    """
    Get Yango Tech product stocks with pagination.

    Use for queries like 'show stocks', 'how much product', 'stocks by stores'.
    Shows product quantities with product names.

    Args:
        cursor: Pagination cursor (obtained from previous response)
        limit: Number of stock records (default 100, maximum 1000)

    Returns:
        Stock batch with pagination information and product names
    """
    try:
        # Ensure products cache is loaded for product name enrichment
        await ensure_products_cache()

        client = get_client()
        async with client:
            response = await client.get_stocks_batch(cursor=cursor, limit=limit)
        enriched_stocks = [enrich_stock_with_product_name(s.model_dump()) for s in response.data]

        result = {
            "stocks": enriched_stocks,
            "pagination": {
                "cursor": response.next_cursor,
                "has_more": response.has_more,
                "total_retrieved": len(enriched_stocks)
            }
        }

        return f"Stock batch (limit: {limit}, retrieved: {len(enriched_stocks)}):\n{json.dumps(result, ensure_ascii=False, indent=2, default=str)}"
    except YangoTechAPIError as e:
        return f"Yango Tech API error: {e}"
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.resource("yango://orders/{order_id}")
async def get_order_resource(order_id: str) -> str:
    """
    Get order details as a resource.

    Args:
        order_id: Order number

    Returns:
        Order details as resource with product names
    """
    try:
        # Ensure products cache is loaded for product name enrichment
        await ensure_products_cache()

        client = get_client()
        async with client:
            order = await client.get_order_details(order_id)
            enriched_order = enrich_order_with_product_names(order.model_dump())
            return json.dumps(enriched_order, ensure_ascii=False, indent=2, default=str)
    except YangoTechAPIError as e:
        return f"API error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.prompt()
def analyze_order(order_id: str) -> str:
    """
    Create prompt for order analysis.

    Args:
        order_id: Order number for analysis

    Returns:
        Prompt for order analysis
    """
    return f"Analyze the status of order {order_id} from Yango Tech and provide detailed recommendations for further actions. Consider all available order data."


@mcp.prompt()
def summarize_products() -> str:
    """
    Create prompt for product analysis.

    Returns:
        Prompt for product catalog analysis
    """
    return "Analyze the Yango Tech product catalog and create a brief report on categories, popularity and recommendations for assortment optimization."


if __name__ == "__main__":
    print("🚀 Starting Yango Tech FastMCP server...")
    print("📋 Available: 6 tools and 2 prompts")
    mcp.run()
