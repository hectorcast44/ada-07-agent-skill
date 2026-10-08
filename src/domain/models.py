from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List

class CustomerTier(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"

@dataclass(frozen=True)
class OrderItem:
    item_id: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self):
        if self.unit_price <= Decimal("0.0"):
            raise ValueError(f"unit_price must be positive, got {self.unit_price}")
        if self.quantity < 1:
            raise ValueError(f"quantity must be >= 1, got {self.quantity}")

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)

@dataclass
class Order:
    order_id: str
    customer_id: str
    tier: CustomerTier
    items: List[OrderItem]

    @property
    def subtotal(self) -> Decimal:
        return sum((item.total_price for item in self.items), Decimal("0.00"))
