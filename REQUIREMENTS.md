# Requirements Specification: Order & Discount Service

## Context
The service calculates order totals, applies promotional and tiered loyalty discounts, and verifies order limits before submitting orders for fulfillment.

## Acceptance Criteria

### AC-01: Tiered Loyalty Discounts
- Customers in tier `BRONZE` receive a 0% discount.
- Customers in tier `SILVER` receive a 5% discount on order subtotal if subtotal >= $50.00.
- Customers in tier `GOLD` receive a 10% discount on order subtotal if subtotal >= $100.00.
- Customers in tier `PLATINUM` receive a 15% discount on order subtotal if subtotal >= $150.00.
- Subtotals below their respective tier threshold do not qualify for the loyalty discount.

### AC-02: Maximum Promotional Cap
- Total applied discounts (loyalty + coupons) cannot exceed 30% of the original subtotal under any circumstances.
- If calculated discount exceeds 30%, it must be clamped exactly to 30.0% of the subtotal.

### AC-03: Security & Validation Boundaries
- Order items must contain positive prices (`price > 0.0`) and positive integer quantities (`quantity >= 1`).
- Customer tier must be strictly validated against the supported enum values (`BRONZE`, `SILVER`, `GOLD`, `PLATINUM`). Any unknown or None tier defaults to `BRONZE` without throwing unhandled exceptions.
- Currency calculations must maintain 2 decimal places precision without floating point drift.

### AC-04: Audit & Determinism
- Order calculations must be pure and reproducible without external side effects during calculation.
