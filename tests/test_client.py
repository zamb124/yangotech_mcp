"""Tests for Yango Tech API HTTP client."""


import pytest

from client import YangoTechAPIError, YangoTechClient
from models import AuthConfig


@pytest.fixture
def auth_config():
    """Authentication configuration fixture."""
    return AuthConfig(
        api_key="test_api_key",
        base_url="https://api.test-yango-tech.com",
        timeout=10,
        max_retries=1
    )


@pytest.fixture
def client(auth_config):
    """Client fixture."""
    return YangoTechClient(auth_config)


class TestYangoTechClient:
    """Tests for Yango Tech API client."""

    @pytest.mark.asyncio
    async def test_client_context_manager(self, client):
        """Test using client as context manager."""
        async with client:
            assert client.client is not None
        # After exiting context, client should be closed
        assert client.client is None or client.client.is_closed

    @pytest.mark.asyncio
    async def test_connect_disconnect(self, client):
        """Test client connection and disconnection."""
        await client.connect()
        assert client.client is not None

        await client.disconnect()
        assert client.client is None or client.client.is_closed

    @pytest.mark.asyncio
    async def test_get_order_details_success(self, client, httpx_mock):
        """Test successful order details retrieval."""
        order_data = {
            "create_time": "2024-09-26T12:50:46.699934+00:00",
            "store_id": "L001",
            "client_phone_number": "+998710000000",
            "payment_type": "cash",
            "payment_status": "pending",
            "delivery_address": {
                "position": {
                    "lat": 41.328088,
                    "lon": 69.314735
                },
                "place_id": "",
                "address": {
                    "country": "-----",
                    "city": "-----",
                    "street": "-----",
                    "house": "-----"
                }
            },
            "use_external_logistics": True,
            "cart": {
                "total_price": "15000",
                "items": [
                    {
                        "product_id": "101030203-00019",
                        "quantity": 1,
                        "price": "1409700",
                        "price_per_quantity": 1
                    }
                ]
            },
            "delivery_properties": {
                "type": "pickup"
            },
            "human_order_id": "240926-099-3407",
            "trace_id": "c4d60bc93a264f7eb7661a9e56c73922"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/orders/get",
            json=order_data,
            status_code=200
        )

        async with client:
            order = await client.get_order_details("240926-099-3407")
            assert order.human_order_id == "240926-099-3407"
            assert order.store_id == "L001"
            assert order.client_phone_number == "+998710000000"
            assert order.cart.total_price == "15000"

    @pytest.mark.asyncio
    async def test_get_order_status_success(self, client, httpx_mock):
        """Test successful order status retrieval."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/orders/state",
            json={
                "query_results": [
                    {
                        "query_result": "success",
                        "state": "delivered"
                    }
                ]
            },
            status_code=200
        )

        async with client:
            status = await client.get_order_status("order123")
            assert status == "delivered"

    @pytest.mark.asyncio
    async def test_get_products_batch_success(self, client, httpx_mock):
        """Test successful product batch retrieval."""
        products_data = {
            "products": [
                {
                    "product_id": "product1",
                    "master_category": "food",
                    "status": "active",
                    "is_meta": False,
                    "custom_attributes": {
                        "shortNameLoc": {"ru_RU": "Product 1"},
                        "barcode": ["1234567890"]
                    }
                },
                {
                    "product_id": "product2",
                    "master_category": "electronics",
                    "status": "active",
                    "is_meta": False,
                    "custom_attributes": {
                        "shortNameLoc": {"ru_RU": "Product 2"},
                        "barcode": ["0987654321"]
                    }
                }
            ],
            "cursor": "cursor123"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/products/query",
            json=products_data,
            status_code=200
        )

        async with client:
            response = await client.get_products_batch(limit=2)
            assert len(response.data) == 2
            assert response.next_cursor == "cursor123"
            assert response.has_more is True
            assert response.total_count is None

    @pytest.mark.asyncio
    async def test_authentication_error(self, client, httpx_mock):
        """Test authentication error handling."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/orders/get",
            status_code=401
        )

        async with client:
            with pytest.raises(YangoTechAPIError) as exc_info:
                await client.get_order_details("order123")

            assert "Authentication error" in str(exc_info.value)
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_not_found_error(self, client, httpx_mock):
        """Test 404 error handling."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/orders/get",
            status_code=404
        )

        async with client:
            with pytest.raises(YangoTechAPIError) as exc_info:
                await client.get_order_details("nonexistent_order")

            assert "Resource not found" in str(exc_info.value)
            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_server_error_with_retry(self, client, httpx_mock):
        """Test server error handling with retries."""
        # First attempt - server error
        httpx_mock.add_response(
            method="POST",
            url="https://api.test-yango-tech.com/b2b/v1/orders/get",
            status_code=500
        )

        async with client:
            with pytest.raises(YangoTechAPIError) as exc_info:
                await client.get_order_details("order123")

            assert "Server error" in str(exc_info.value)
            assert exc_info.value.status_code == 500
