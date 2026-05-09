"""Deterministic economic reasoning checks for Signal scenarios and results."""

from __future__ import annotations

from typing import Any


CARE_SUFFIXES = {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}
SUPPORTED_SIMULATION_TYPES = {"sam_multiplier", "scenario_comparison", "baseline"}
SUPPORTED_CLOSURES = {
    "standard_sam_multiplier",
    "government_savings_adjusts",
    "investment_driven_with_fixed_prices",
    "external_account_adjusts",
}


def validate_policy_shock(scenario: dict[str, Any]) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    accounts = scenario.get("target_accounts") or [scenario.get("shock_account")]
    shock_size = float(scenario.get("shock_size", scenario.get("shock_value", 0)) or 0)
    shock_type = str(scenario.get("shock_type", ""))
    closure = scenario.get("closure", scenario.get("closure_rule", "standard_sam_multiplier"))
    simulation_type = scenario.get("simulation_type", "sam_multiplier")

    if not accounts or not accounts[0]:
        errors.append("Missing shock account.")
    if shock_size < 0 and shock_type not in {"tax"}:
        warnings.append("Negative shock size should be explicitly justified.")
    if simulation_type not in SUPPORTED_SIMULATION_TYPES:
        errors.append(f"Unsupported simulation type: {simulation_type}.")
    if closure not in SUPPORTED_CLOSURES:
        errors.append(f"Unsupported closure: {closure}.")
    if "care" in shock_type:
        present = {str(account).lower() for account in accounts}
        missing = sorted(CARE_SUFFIXES.difference(present))
        if missing:
            warnings.append("Care-economy scenario does not include all gender-care suffixes: " + ", ".join(missing))
    warnings.append("GAMS is optional; if unavailable, Signal will use the Python SAM multiplier fallback.")
    warnings.append("Python fallback is a SAM multiplier screen, not a full CGE equilibrium solution.")
    warnings.extend(scenario.get("validation_warnings", []))
    return {"valid": not errors, "errors": errors, "warnings": _dedupe(warnings)}


def explain_transmission_channels(scenario: dict[str, Any]) -> list[str]:
    shock_type = scenario.get("shock_type", "")
    if shock_type in {"government_spending", "public_investment", "care_infrastructure"}:
        return [
            "Government demand increases output in targeted services and linked suppliers.",
            "Multiplier effects transmit to labour income, household income, and government accounts.",
        ]
    if shock_type == "tax":
        return [
            "Tax changes alter user costs, disposable income, government revenue, and sector demand.",
            "Distributional effects depend on which households consume or earn income from targeted sectors.",
        ]
    if shock_type == "trade_facilitation":
        return ["Lower trade frictions raise export demand and transmit through domestic supply chains."]
    if "care" in shock_type:
        return ["Care shocks affect paid services, unpaid-care substitution, gendered labour income, and household welfare."]
    if "infrastructure" in shock_type or shock_type == "productivity":
        return ["Infrastructure and productivity shocks lower effective costs and raise linked sector output."]
    return ["The scenario transmits through SAM account linkages using fixed-price multiplier relationships."]


def flag_possible_inconsistencies(results: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    diagnostics = results.get("diagnostics", {}) if isinstance(results, dict) else {}
    for block in diagnostics.values():
        if isinstance(block, dict):
            warnings.extend(str(item) for item in block.get("warnings", []))
    output_results = results.get("results", {}) if isinstance(results, dict) else {}
    if not output_results.get("households"):
        warnings.append("Household accounts were not clearly identified in the result set.")
    if not output_results.get("factors"):
        warnings.append("Factor accounts were not clearly identified in the result set.")
    return _dedupe(warnings)


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))
