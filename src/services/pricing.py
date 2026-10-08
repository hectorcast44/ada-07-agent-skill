from decimal import Decimal, ROUND_HALF_UP
from src.domain.models import CustomerTier, Order

class PricingService:
    @staticmethod
    def calculate_subtotal(order: Order) -> Decimal:
        return order.subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_final_total(order: Order) -> Decimal:
        # Baseline before loyalty discount feature PR #42
        return PricingService.calculate_subtotal(order)
