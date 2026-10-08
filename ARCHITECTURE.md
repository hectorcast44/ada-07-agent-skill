# Architecture Guidelines

## Architecture Overview
This service follows a modular, layered architecture:

- `src/domain/`: Pure domain entities and value objects (models, pricing rules, invariants). Free of external I/O or frameworks.
- `src/services/`: Application services coordinating business workflows (discount calculation, validation, receipt formatting).
- `tests/`: Automated unit and integration test suites using pytest.

## Boundaries and Rules
1. **Domain Isolation**: Domain logic in `src/domain/` must never import from delivery or external infrastructure layers.
2. **Determinism**: Calculations must use `decimal.Decimal` or integer cents to avoid floating-point errors.
3. **Immutability**: Domain models should prefer dataclasses or frozen attributes where appropriate.
4. **Error Handling**: Input validation errors must return structured `ValueError` or custom domain exceptions, not raw stack traces.
