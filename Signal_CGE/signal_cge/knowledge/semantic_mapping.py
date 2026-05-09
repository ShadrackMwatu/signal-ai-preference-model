"""Deterministic semantic mappings for Signal CGE scenario interpretation."""

from __future__ import annotations

from typing import Any


SEMANTIC_SCENARIO_MAP = {
    "tariff": {
        "simulation_type": "trade_policy",
        "policy_instrument": "import_tariff",
        "references": ["trade_block", "government_revenue", "price_transmission"],
    },
    "vat": {
        "simulation_type": "tax_policy",
        "policy_instrument": "vat_tax",
        "references": ["government_revenue", "household_demand", "price_transmission"],
    },
    "care": {
        "simulation_type": "care_economy",
        "policy_instrument": "care_investment",
        "references": ["investment_savings", "factor_market", "household_welfare"],
    },
    "exports": {
        "simulation_type": "trade_policy",
        "policy_instrument": "export_demand",
        "references": ["trade_block", "market_clearing", "price_transmission"],
    },
    "productivity": {
        "simulation_type": "productivity",
        "policy_instrument": "productivity_shock",
        "references": ["production_block", "factor_market", "recursive_dynamics"],
    },
}


def map_prompt_semantics(prompt: str, scenario: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return deterministic semantic hints from prompt text and parsed scenario."""

    text = (prompt or "").lower()
    matched = []
    merged: dict[str, Any] = {"semantic_matches": matched, "reference_hints": []}
    for keyword, mapping in SEMANTIC_SCENARIO_MAP.items():
        if keyword in text:
            matched.append(keyword)
            merged.setdefault("simulation_type", mapping["simulation_type"])
            merged.setdefault("policy_instrument", mapping["policy_instrument"])
            merged["reference_hints"].extend(mapping["references"])
    if scenario:
        merged["parsed_simulation_type"] = scenario.get("simulation_type")
        merged["parsed_shock_type"] = scenario.get("shock_type")
    merged["reference_hints"] = sorted(set(merged["reference_hints"]))
    return merged


def infer_account_type(account: str) -> str:
    """Infer broad account type from Signal naming conventions."""

    normalized = (account or "").lower()
    if normalized.startswith("c"):
        return "commodity"
    if normalized.startswith("a"):
        return "activity"
    if normalized in {"government", "gov"} or "gov" in normalized:
        return "government"
    if "household" in normalized or normalized.startswith("hh"):
        return "household"
    if normalized in {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}:
        return "gender_care_factor"
    return "unknown"
