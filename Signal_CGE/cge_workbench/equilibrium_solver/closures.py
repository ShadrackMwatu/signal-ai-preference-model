"""Closure rules for the Signal Static CGE Solver."""

from __future__ import annotations

from typing import Any


DEFAULT_CLOSURE = {
    "savings_investment": "savings_driven_investment",
    "government": "fixed_government_consumption_shares",
    "external": "fixed_foreign_savings",
    "numeraire": "fixed_commodity_price",
    "factor_market": "flexible_factor_return",
}

SUPPORTED_CLOSURES = {
    "savings_investment": {"savings_driven_investment"},
    "government": {"fixed_government_consumption_shares"},
    "external": {"fixed_foreign_savings"},
    "numeraire": {"fixed_commodity_price"},
    "factor_market": {"flexible_factor_return", "fixed_factor_supply"},
}


def normalize_closure(closure: dict[str, Any] | None = None) -> dict[str, str]:
    """Return a complete closure dictionary with defaults applied."""

    normalized = dict(DEFAULT_CLOSURE)
    for key, value in (closure or {}).items():
        if key in normalized:
            normalized[key] = str(value)
    validation = validate_closure(normalized)
    if not validation["valid"]:
        raise ValueError("; ".join(validation["errors"]))
    return normalized


def validate_closure(closure: dict[str, Any] | None = None) -> dict[str, Any]:
    """Check whether selected closure names are supported."""

    closure = {**DEFAULT_CLOSURE, **(closure or {})}
    errors: list[str] = []
    for family, selected in closure.items():
        if family in SUPPORTED_CLOSURES and selected not in SUPPORTED_CLOSURES[family]:
            errors.append(f"Unsupported {family} closure: {selected}")
    return {"valid": not errors, "errors": errors, "closure": closure}
