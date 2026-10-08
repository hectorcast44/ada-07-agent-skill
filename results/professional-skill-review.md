# Multi-Axis Code Review: PR #42 Tiered Discounts

**Skill Used**: `code-review-and-quality` (addyosmani/agent-skills)  
**Target**: PR #42 (`feature/pr-42-tiered-discounts` -> `main`)  
**Context**: Evaluated against `REQUIREMENTS.md`, `ARCHITECTURE.md`, full `git diff`, and pytest execution evidence.  
**Mode**: Draft-Only / Human Review. No remote modifications or automatic merges performed.

---

## 1. Review Context & Executive Summary

The PR introduces tiered loyalty discount calculations for customers (`BRONZE`, `SILVER`, `GOLD`, `PLATINUM`) and applies a 30% maximum promotional cap. While the core calculations pass basic happy-path unit tests (5 passed in 0.01s), the multi-axis review reveals a functional correctness bug in the boundary condition for the `SILVER` tier, a regression caused by the deletion of previous negative test cases, and a missing input validation guard.

**Verdict**: **Request changes** — Critical and Required issues must be addressed before merge.

---

## 2. Five-Axis Assessment

### Axis 1: Correctness
- **Finding 1.1**: Off-by-one threshold comparison for `CustomerTier.SILVER`.
  - **Severity**: Critical (Blocks merge)
  - **File / Evidence**: `src/services/pricing.py#L35` (`if subtotal > min_threshold:`)
  - **Engineering Rationale**: Specification AC-01 explicitly mandates: *"Customers in tier SILVER receive a 5% discount on order subtotal if subtotal >= $50.00"*. Using strict inequality (`>`) causes an order with exactly $50.00 to receive $0.00 discount instead of the expected $2.50.
  - **Recommended Action**: Replace `if subtotal > min_threshold:` with `if subtotal >= min_threshold:` or unify the logic across all tiers. Add a unit test asserting an exact $50.00 subtotal order.

- **Finding 1.2**: Insufficient boundary testing in test suite.
  - **Severity**: Required change
  - **File / Evidence**: `tests/test_pricing.py#L36-L40` (`test_silver_tier_above_threshold_discount`)
  - **Engineering Rationale**: The test only exercises $60.00 subtotal, leaving the boundary condition ($50.00) unverified. Under mutation testing guidelines, an inverted boundary condition in the code does not fail this test suite.
  - **Recommended Action**: Add boundary test cases for $49.99 (0% discount) and $50.00 (5% discount).

### Axis 2: Readability & Simplicity
- **Finding 2.1**: Unnecessary conditional branching for `SILVER` tier.
  - **Severity**: Consider / Refactoring suggestion
  - **File / Evidence**: `src/services/pricing.py#L34-L44`
  - **Engineering Rationale**: The code duplicates the discount calculation structure between `if tier == CustomerTier.SILVER:` and the `else:` branch. Once the boundary comparison is fixed to `>= min_threshold`, the special-case `if` becomes completely redundant.
  - **Recommended Action**: Collapse the two branches into a single uniform statement:
    ```python
    if subtotal >= min_threshold:
        discount = subtotal * rate
    else:
        discount = Decimal("0.00")
    ```

### Axis 3: Architecture
- **Finding 3.1**: Mutable module-level configuration dictionaries.
  - **Severity**: Nit / Optional
  - **File / Evidence**: `src/services/pricing.py#L5-L17` (`TIER_RATES`, `TIER_MIN_THRESHOLDS`)
  - **Engineering Rationale**: Global mutable dictionaries can be mutated by external modules or during concurrent execution, violating pure domain isolation principles defined in `ARCHITECTURE.md`.
  - **Recommended Action**: Type with `typing.Final` and wrap with `MappingProxyType` or encapsulate inside a dedicated domain pricing policy object.

### Axis 4: Security
- **Finding 4.1**: Missing boundary input validation on external parameter `coupon_discount`.
  - **Severity**: Required change
  - **File / Evidence**: `src/services/pricing.py#L52` (`calculate_final_total`)
  - **Engineering Rationale**: Data from external parameters must be treated as untrusted. If an upstream caller supplies a negative `Decimal("-20.00")`, the calculation `total_discount = loyalty_discount + coupon_discount` reduces total discount or inflates pricing without validation.
  - **Recommended Action**: Guard the parameter at the entry boundary:
    ```python
    if coupon_discount is not None and coupon_discount < Decimal("0.00"):
        raise ValueError("coupon_discount cannot be negative")
    ```

### Axis 5: Performance
- **Assessment**: The computation complexity is \(O(N)\) over order items with fast decimal arithmetic. Memory allocations are bounded. No N+1 patterns or unconstrained loops exist. **Status**: PASS.

---

## 3. Verification & Test Hygiene

- **Finding V.1**: Regressive deletion of baseline validation tests.
  - **Severity**: Critical (Blocks merge)
  - **File / Evidence**: `tests/test_pricing.py` diff
  - **Engineering Rationale**: `git diff` shows that `test_negative_item_price_raises_error` and `test_zero_quantity_raises_error` were deleted. Removing negative validation tests degrades the verification safety net.
  - **Recommended Action**: Revert the test deletions and maintain full coverage of domain invariants.

---

## 4. Skill Composition & Delegation
- **Delegated Capabilities**:
  - Deep-dive vulnerability scanning and dependency audit: Recommends invoking `security-and-hardening`.
  - Formal mutation score analysis: Recommends invoking `constraint-driven-development`.

---

## 5. Review Summary & Quality Gates

| Severity Category | Count | Status |
|---|---|---|
| **Critical** (Blocks merge) | 2 | Action required before merge |
| **Required change** (Must address) | 2 | Action required before merge |
| **Consider / Optional** | 1 | Non-blocking recommendation |
| **Nit** | 1 | Non-blocking style suggestion |

**Quality Gate Decision**: **CHANGES REQUESTED**  
**Human Decision Required**: **YES** (Delegated to human maintainer for final approval after fixes).
