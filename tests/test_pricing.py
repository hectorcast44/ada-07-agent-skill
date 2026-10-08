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

def test_gold_tier_discount_applied():
    items = [
        OrderItem("item-1", Decimal("50.00"), 2),  # subtotal = 100.00
    ]
    order = Order("ord-102", "cust-2", CustomerTier.GOLD, items)
    assert PricingService.calculate_loyalty_discount(order) == Decimal("10.00")
    assert PricingService.calculate_final_total(order) == Decimal("90.00")

def test_platinum_tier_discount_applied():
    items = [
        OrderItem("item-1", Decimal("200.00"), 1),  # subtotal = 200.00
    ]
    order = Order("ord-103", "cust-3", CustomerTier.PLATINUM, items)
    # 15% of 200 = 30.00
    assert PricingService.calculate_loyalty_discount(order) == Decimal("30.00")
    assert PricingService.calculate_final_total(order) == Decimal("170.00")

def test_max_cap_clamps_excessive_coupon():
    items = [
        OrderItem("item-1", Decimal("100.00"), 1),  # subtotal = 100.00
    ]
    order = Order("ord-104", "cust-4", CustomerTier.GOLD, items)  # loyalty = 10.00
    # Coupon = 25.00 -> total nominal = 35.00, cap is 30% = 30.00
    assert PricingService.calculate_final_total(order, coupon_discount=Decimal("25.00")) == Decimal("70.00")

def test_silver_tier_above_threshold_discount():
    # Subtotal 60.00 > 50.00
    items = [OrderItem("item-1", Decimal("60.00"), 1)]
    order = Order("ord-105", "cust-5", CustomerTier.SILVER, items)
    assert PricingService.calculate_loyalty_discount(order) == Decimal("3.00")
