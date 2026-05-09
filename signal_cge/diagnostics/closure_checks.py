"""Closure diagnostics for Signal simulations."""

from __future__ import annotations

from typing import Any


SUPPORTED_CLOSURES = {
    "standard_sam_multiplier",
    "government_savings_adjusts",
    "investment_driven_with_fixed_prices",
    "external_account_adjusts",
}


def validate_closure(scenario: dict[str, Any]) -> dict[str, Any]:
    closure = scenario.get("closure_rule", "standard_sam_multiplier")
    warnings = []
    errors = []
    if closure not in SUPPORTED_CLOSURES:
        errors.append(f"Unsupported closure rule: {closure}")
    if scenario.get("shock_type") == "tax" and closure != "government_savings_adjusts":
        warnings.append("Tax scenarios should state how government balance adjusts.")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "closure_rule": closure}
