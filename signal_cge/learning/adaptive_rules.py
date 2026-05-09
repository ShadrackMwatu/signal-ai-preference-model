"""Deterministic adaptive interpretation rules for Signal CGE prompts."""

from __future__ import annotations

import re
from typing import Any


def apply_adaptive_prompt_rules(prompt: str, scenario: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return deterministic rule hints that improve prompt interpretation."""

    text = (prompt or "").lower()
    target = _extract_target(text)
    hints: dict[str, Any] = {"prompt": prompt, "rules_applied": []}
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
        if target.startswith("c"):
            hints["target_account_type"] = "commodity"
            hints["rules_applied"].append("c_prefix_to_commodity")
        elif target.startswith("a"):
            hints["target_account_type"] = "activity"
            hints["rules_applied"].append("a_prefix_to_activity")
    if scenario:
        hints["scenario_type"] = scenario.get("shock_type") or scenario.get("simulation_type")
    return hints


def _extract_target(text: str) -> str:
    match = re.search(r"\bon\s+([a-zA-Z][a-zA-Z0-9_/-]*)", text)
    return match.group(1).strip(" .,/;:") if match else ""
