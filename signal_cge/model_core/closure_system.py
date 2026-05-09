"""Closure rule registry for the formal Signal CGE model."""

from __future__ import annotations

from typing import Any


SUPPORTED_CLOSURES = {
    "savings_driven_investment": "Investment adjusts to available savings.",
    "government_deficit_closure": "Government savings or deficit adjusts to fiscal balance.",
    "foreign_savings_exchange_rate": "Foreign savings or exchange rate adjusts external balance.",
    "consumer_price_numeraire": "Consumer price index is the price numeraire.",
    "fixed_factor_supply": "Factor supply is fixed and factor prices clear markets.",
}


DEFAULT_CLOSURE = {
    "investment_savings": "savings_driven_investment",
    "government": "government_deficit_closure",
    "external": "foreign_savings_exchange_rate",
    "numeraire": "consumer_price_numeraire",
    "factor_market": "fixed_factor_supply",
}


def validate_closure_rules(closure: dict[str, str] | None = None) -> dict[str, Any]:
    """Validate closure choices against the supported Signal closure registry."""

    selected = {**DEFAULT_CLOSURE, **(closure or {})}
    errors = []
    for dimension, rule in selected.items():
        if rule not in SUPPORTED_CLOSURES:
            errors.append(f"Unsupported closure rule for {dimension}: {rule}")
    return {"valid": not errors, "errors": errors, "closure": selected}


def describe_closure_rules() -> dict[str, str]:
    return SUPPORTED_CLOSURES.copy()
