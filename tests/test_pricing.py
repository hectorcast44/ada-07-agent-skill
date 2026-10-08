import pytest
from decimal import Decimal
from src.domain.models import CustomerTier, OrderItem, Order
from src.services.pricing import PricingService

def test_order_subtotal_calculation():
    items = [
        OrderItem("item-1", Decimal("20.00"), 2),
        OrderItem("item-2", Decimal("15.50"), 1),
    ]
    order = Order("ord-101", "cust-1", CustomerTier.BRONZE, items)
    assert PricingService.calculate_subtotal(order) == Decimal("55.50")

def test_negative_item_price_raises_error():
    with pytest.raises(ValueError):
        OrderItem("item-bad", Decimal("-10.00"), 1)

def test_zero_quantity_raises_error():
    with pytest.raises(ValueError):
        OrderItem("item-bad", Decimal("10.00"), 0)
