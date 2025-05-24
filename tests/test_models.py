"""Tests for Yango Tech data models."""

from datetime import datetime
from decimal import Decimal

from models import (
    Address,
    AuthConfig,
    Cart,
    CartItem,
    DeliveryAddress,
    DeliveryProperties,
    Order,
    Position,
    Price,
    Product,
    Stock,
    Store,
)


class TestAuthConfig:
    """Tests for authentication configuration."""

    def test_auth_config_creation(self):
        """Test authentication configuration creation."""
        config = AuthConfig(api_key="test_key")

        assert config.api_key == "test_key"
        assert config.base_url == "https://api.retailtech.yango.com"
        assert config.timeout == 30
        assert config.max_retries == 3


class TestProduct:
    """Tests for product model."""

    def test_product_creation(self):
        """Test product creation."""
        product = Product(
            product_id="12345",
            master_category="food",
            status="active",
            is_meta=False,
            custom_attributes={
                "shortNameLoc": {"ru_RU": "Test Product"},
                "barcode": ["1234567890"]
            }
        )

        assert product.product_id == "12345"
        assert product.master_category == "food"
        assert product.status == "active"
        assert product.is_meta is False
        assert product.name == "Test Product"
        assert product.barcode == ["1234567890"]

    def test_product_name_priority_english_first(self):
        """Test that English (en_EN) is prioritized for product name."""
        product = Product(
            product_id="12345",
            master_category="food",
            status="active",
            is_meta=False,
            custom_attributes={
                "shortNameLoc": {
                    "ru_RU": "Тестовый продукт",
                    "en_EN": "Test Product EN",
                    "uz_UZ": "Test mahsulot"
                },
                "longName": {
                    "ru_RU": "Длинное имя продукта",
                    "en_EN": "Long Product Name EN",
                    "fr_FR": "Nom de produit long"
                }
            }
        )

        # Should pick English versions
        assert product.name == "Test Product EN"
        assert product.long_name == "Long Product Name EN"

    def test_product_name_fallback_any_language(self):
        """Test that any available language is used when en_EN is not available."""
        product = Product(
            product_id="12345",
            master_category="food",
            status="active",
            is_meta=False,
            custom_attributes={
                "shortNameLoc": {
                    "de_DE": "Testprodukt",
                    "fr_FR": "Produit de test"
                },
                "longName": {
                    "ja_JP": "テスト製品",
                    "it_IT": "Prodotto di prova"
                }
            }
        )

        # Should pick first available (order may vary)
        assert product.name in ["Testprodukt", "Produit de test"]
        assert product.long_name in ["テスト製品", "Prodotto di prova"]

    def test_product_name_empty_values_handled(self):
        """Test that empty values are skipped properly."""
        product = Product(
            product_id="12345",
            master_category="food",
            status="active",
            is_meta=False,
            custom_attributes={
                "shortNameLoc": {
                    "en_EN": "",  # Empty string should be skipped
                    "ru_RU": "Тестовый продукт"
                },
                "longName": {
                    "en_EN": None,  # None should be skipped
                    "ru_RU": "Длинное имя"
                }
            }
        )

        # Should skip empty en_EN and pick ru_RU
        assert product.name == "Тестовый продукт"
        assert product.long_name == "Длинное имя"


class TestPrice:
    """Tests for price model."""

    def test_price_creation(self):
        """Test price creation."""
        now = datetime.now()
        price = Price(
            product_id="12345",
            store_id="67890",
            price=Decimal("99.99"),
            updated_at=now
        )

        assert price.product_id == "12345"
        assert price.store_id == "67890"
        assert price.price == Decimal("99.99")
        assert price.currency == "RUB"
        assert price.updated_at == now


class TestStock:
    """Tests for stock model."""

    def test_stock_creation(self):
        """Test stock creation."""
        stock = Stock(
            product_id="12345",
            store_id="67890",
            quantity=100,
            shelf_type="store"
        )

        assert stock.product_id == "12345"
        assert stock.store_id == "67890"
        assert stock.quantity == 100
        assert stock.shelf_type == "store"


class TestStore:
    """Tests for store model."""

    def test_store_creation(self):
        """Test store creation."""
        store = Store(
            id="store123",
            name="Test Store",
            address="Test Street, 1",
            city="Moscow"
        )

        assert store.id == "store123"
        assert store.name == "Test Store"
        assert store.address == "Test Street, 1"
        assert store.city == "Moscow"
        assert store.is_active is True


class TestOrder:
    """Tests for order model."""

    def test_order_creation(self):
        """Test order creation."""
        delivery_address = DeliveryAddress(
            position=Position(lat=41.328088, lon=69.314735),
            place_id="place123",
            address=Address(
                country="Uzbekistan",
                city="Tashkent",
                street="Test Street",
                house="10"
            )
        )

        order_item = CartItem(
            product_id="product123",
            quantity=2,
            price="50.00",
            price_per_quantity=1
        )

        cart = Cart(
            total_price="100.00",
            items=[order_item]
        )

        delivery_properties = DeliveryProperties(type="pickup")

        order = Order(
            create_time="2024-09-26T12:50:46.699934+00:00",
            store_id="store123",
            client_phone_number="+998710000000",
            payment_type="cash",
            payment_status="pending",
            delivery_address=delivery_address,
            use_external_logistics=True,
            cart=cart,
            delivery_properties=delivery_properties,
            human_order_id="240926-099-3407",
            trace_id="c4d60bc93a264f7eb7661a9e56c73922"
        )

        assert order.human_order_id == "240926-099-3407"
        assert order.store_id == "store123"
        assert order.client_phone_number == "+998710000000"
        assert order.payment_type == "cash"
        assert order.payment_status == "pending"
        assert order.cart.total_price == "100.00"
        assert len(order.cart.items) == 1
        assert order.id == "240926-099-3407"
        assert order.total_amount == "100.00"
