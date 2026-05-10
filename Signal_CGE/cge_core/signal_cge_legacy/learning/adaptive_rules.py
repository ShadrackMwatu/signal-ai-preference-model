"""Deterministic adaptive interpretation rules for Signal CGE prompts."""

from __future__ import annotations

import re
from typing import Any

from ..knowledge.semantic_mapping import infer_account_type
from .scenario_pattern_learning import learn_prompt_patterns


def apply_adaptive_prompt_rules(prompt: str, scenario: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return deterministic rule hints that improve prompt interpretation."""

    text = (prompt or "").lower()
    target = _extract_target(text)
    learned_patterns = learn_prompt_patterns(limit=100)
    hints: dict[str, Any] = {"prompt": prompt, "rules_applied": [], "learned_patterns": learned_patterns}
    if "tariff" in text and ("reduce" in text or "lower" in text or "cut" in text):
        hints.update(
            {
                "policy_instrument": "import_tariff",
                "shock_direction": "decrease",
                "target_account": target,
                "simulation_type": "trade_policy",
            }
        )
        hints["rules_applied"].append("reduce_tariff_to_import_tariff_decrease")
    if "vat" in text and "increase" in text:
        hints.update({"policy_instrument": "vat_tax", "shock_direction": "increase", "simulation_type": "tax_policy"})
        hints["rules_applied"].append("increase_vat_to_tax_policy")
    if "care" in text:
        hints["activate_gender_care_reporting"] = True
        hints["rules_applied"].append("care_prompt_to_gender_care_reporting")
    if target:
        account_type = infer_account_type(target)
        hints["target_account_type"] = account_type
        if account_type != "unknown":
            hints["rules_applied"].append(f"{account_type}_account_inference")
    if "double" in text and "care" in text:
        hints.update({"policy_instrument": "care_investment", "shock_direction": "increase", "shock_size_hint": 100})
        hints["rules_applied"].append("double_care_to_100_percent_investment_shock")
    if "boost" in text and "export" in text:
        hints.update({"policy_instrument": "export_demand", "shock_direction": "increase", "simulation_type": "trade_policy"})
        hints["rules_applied"].append("boost_exports_to_export_demand_scenario")
    if scenario:
        hints["scenario_type"] = scenario.get("shock_type") or scenario.get("simulation_type")
    return hints


def evolve_adaptive_rules_from_memory(limit: int = 100) -> dict[str, Any]:
    """Return deterministic rule evolution proposals from observed prompt patterns."""

    patterns = learn_prompt_patterns(limit=limit)
    proposals: list[str] = []
    prompt_terms = patterns.get("common_prompt_terms", [])
    terms = {term for term, _count in prompt_terms}
    if {"tariffs", "tariff"}.intersection(terms):
        proposals.append("Keep mapping tariff reduction prompts to import_tariff decrease scenarios.")
    if "vat" in terms:
        proposals.append("Keep mapping VAT prompts to government tax-revenue and price channels.")
    if "care" in terms:
        proposals.append("Keep activating gender-care reporting for care prompts.")
    if "exports" in terms or "export" in terms:
        proposals.append("Add richer export-demand scenario templates.")
    return {"learned_patterns": patterns, "rule_evolution_proposals": proposals}


def _extract_target(text: str) -> str:
    match = re.search(r"\bon\s+([a-zA-Z][a-zA-Z0-9_/-]*)", text)
    return match.group(1).strip(" .,/;:") if match else ""
