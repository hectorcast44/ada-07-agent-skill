# PR Readiness Review

## Review Context
PR / Branch: PR #42 (feature/pr-42-tiered-discounts -> main)
Reviewer Agent: Antigravity Code Review Agent (Skill: reviewing-pull-requests v1.0.0)
Date: 2026-10-08

## Requirements / Acceptance Criteria Reviewed
- **AC-01: Tiered Loyalty Discounts**: BRONZE 0%, SILVER 5% (threshold >= $50.00), GOLD 10% (threshold >= $100.00), PLATINUM 15% (threshold >= $150.00). Subtotals below threshold receive 0%.
- **AC-02: Maximum Promotional Cap**: Total discounts capped strictly at 30% of subtotal.
- **AC-03: Security & Validation Boundaries**: Item price > 0, quantity >= 1, valid tiers, Decimal 2-decimal precision.
- **AC-04: Audit & Determinism**: Pure calculation without external side-effects.

## Test Evidence
- Command executed: `pytest -v`
- Result: 5 passed in 0.01s (exit code 0).
- Suite observation: Tests cover happy path for GOLD (100.00), PLATINUM (200.00), and max coupon cap (30%). However, boundary testing for SILVER threshold ($50.00 exact) was omitted, and baseline negative validation tests were removed.

## MUST FIX

### RF-01
Requirement / AC: AC-01 (Tiered Loyalty Discounts - SILVER boundary)
File: `src/services/pricing.py#L35`
Evidence: Line 35 implements `if subtotal > min_threshold:` specifically for `CustomerTier.SILVER`, whereas lines 41 implements `>= min_threshold` for other tiers.
Problem: When an order subtotal is exactly $50.00 for a SILVER customer, discount evaluates to $0.00 instead of $2.50 (5%), violating AC-01.
Recommended next step: Change condition to `if subtotal >= min_threshold:` (or eliminate the redundant special case branch for SILVER) and add a test case in `tests/test_pricing.py` asserting that subtotal of $50.00 yields $2.50 discount.

### RF-02
Requirement / AC: AC-03 & Test Suite Integrity (Non-weakening of test suite)
File: `tests/test_pricing.py`
Evidence: Diff inspection shows that `test_negative_item_price_raises_error` and `test_zero_quantity_raises_error` present in `main` were deleted in this branch.
Problem: Removes existing test coverage for negative pricing and zero quantity validations, violating the core checklist rule "Existing behavior is not weakened".
Recommended next step: Restore the deleted baseline tests in `tests/test_pricing.py`.

## SHOULD FIX

### SF-01
Requirement / AC: AC-03 (Validation Boundaries)
File: `src/services/pricing.py#L52`
Evidence: `calculate_final_total` takes `coupon_discount: Optional[Decimal] = None` without checking whether `coupon_discount < Decimal("0.00")`.
Problem: Supplying a negative coupon discount artificially inflates the total without raising a domain validation error.
Recommended next step: Add guard check `if coupon_discount is not None and coupon_discount < Decimal("0.00"): raise ValueError("coupon_discount cannot be negative")`.

## OPTIONAL

### OP-01
Requirement / AC: Code Quality & Typing Best Practices
File: `src/services/pricing.py#L5-L17`
Evidence: `TIER_RATES` and `TIER_MIN_THRESHOLDS` are defined as plain dicts.
Problem: Could be marked immutable using `typing.Final` and `Mapping` to prevent accidental runtime modification.
Recommended next step: Annotate as `Final[Mapping[CustomerTier, Decimal]]`.

## Open Questions
- Should coupon discounts be tracked as a dedicated Value Object / domain entity in a future PR as specified in `ARCHITECTURE.md`?

## Final Review Summary
MUST FIX count: 2
SHOULD FIX count: 1
OPTIONAL count: 1

Human decision required:
YES
