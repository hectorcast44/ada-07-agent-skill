from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from src.domain.models import CustomerTier, Order

TIER_RATES = {
    CustomerTier.BRONZE: Decimal("0.00"),
    CustomerTier.SILVER: Decimal("0.05"),
    CustomerTier.GOLD: Decimal("0.10"),
    CustomerTier.PLATINUM: Decimal("0.15"),
}

TIER_MIN_THRESHOLDS = {
    CustomerTier.BRONZE: Decimal("0.00"),
    CustomerTier.SILVER: Decimal("50.00"),
    CustomerTier.GOLD: Decimal("100.00"),
    CustomerTier.PLATINUM: Decimal("150.00"),
}

MAX_DISCOUNT_RATIO = Decimal("0.30")

class PricingService:
    @staticmethod
    def calculate_subtotal(order: Order) -> Decimal:
        return order.subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_loyalty_discount(order: Order) -> Decimal:
        subtotal = PricingService.calculate_subtotal(order)
        tier = order.tier if isinstance(order.tier, CustomerTier) else CustomerTier.BRONZE
        
        rate = TIER_RATES.get(tier, Decimal("0.00"))
        min_threshold = TIER_MIN_THRESHOLDS.get(tier, Decimal("0.00"))

        # NOTE: Off-by-one bug here for SILVER tier: strictly greater than instead of >=
        if tier == CustomerTier.SILVER:
            if subtotal > min_threshold:
                discount = subtotal * rate
            else:
                discount = Decimal("0.00")
        else:
            if subtotal >= min_threshold:
                discount = subtotal * rate
            else:
                discount = Decimal("0.00")

        # AC-02 Max cap check
        max_discount = (subtotal * MAX_DISCOUNT_RATIO).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        discount = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return min(discount, max_discount)

    @staticmethod
    def calculate_final_total(order: Order, coupon_discount: Optional[Decimal] = None) -> Decimal:
        subtotal = PricingService.calculate_subtotal(order)
        loyalty_discount = PricingService.calculate_loyalty_discount(order)
        total_discount = loyalty_discount + (coupon_discount or Decimal("0.00"))
        
        max_discount = (subtotal * MAX_DISCOUNT_RATIO).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        effective_discount = min(total_discount, max_discount)
        
        final_total = subtotal - effective_discount
        return final_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
