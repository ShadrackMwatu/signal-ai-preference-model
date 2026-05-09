"""Closure manager for Signal CGE macro and market-clearing assumptions."""

from __future__ import annotations

from typing import Any


CLOSURE_OPTIONS: dict[str, dict[str, str]] = {
    "base_closure": {"investment": "savings_driven", "government": "fixed_government_savings", "external": "fixed_foreign_savings", "factor_market": "full_employment"},
    "static_comparative_closure": {"investment": "savings_driven", "government": "flexible_direct_tax_replacement", "external": "flexible_exchange_rate", "factor_market": "full_employment"},
    "recursive_dynamic_closure": {"investment": "investment_driven_savings", "government": "fixed_government_savings", "external": "fixed_foreign_savings", "factor_market": "labor_growth_supply"},
    "savings_driven_investment": {"investment": "savings_driven"},
    "investment_driven_savings": {"investment": "investment_driven_savings"},
    "fixed_government_savings": {"government": "fixed_government_savings"},
    "flexible_direct_tax_replacement": {"government": "flexible_direct_tax_replacement"},
    "fixed_foreign_savings": {"external": "fixed_foreign_savings"},
    "flexible_exchange_rate": {"external": "flexible_exchange_rate"},
    "factor_full_employment": {"factor_market": "full_employment"},
    "unemployment_fixed_wage": {"factor_market": "fixed_wage_unemployment"},
}


def get_closure_options() -> dict[str, dict[str, str]]:
    return CLOSURE_OPTIONS.copy()


def validate_closure(closure_name: str, required_variables: list[str] | None = None) -> dict[str, Any]:
    """Validate a known closure and flag missing closure variables."""

    settings = CLOSURE_OPTIONS.get(closure_name)
    missing_variables = []
    if required_variables:
        known_text = " ".join(settings.values()) if settings else ""
        missing_variables = [variable for variable in required_variables if variable not in known_text]
    return {
        "valid": settings is not None and not missing_variables,
        "closure_name": closure_name,
        "settings": settings or {},
        "missing_closure_variables": missing_variables,
        "warnings": [] if settings else [f"Unsupported closure: {closure_name}"],
    }


def default_closure_payload(closure_name: str = "base_closure") -> dict[str, Any]:
    validation = validate_closure(closure_name)
    return {"closure": closure_name, "settings": validation["settings"], "validation": validation}
