"""Compact policy summary service for Signal AI CGE Chat Studio."""

from __future__ import annotations

from typing import Any

from policy_ai.scenario_recommender import recommend_next_scenarios
from signal_ai.explainability.mechanism_explainer import explain_mechanism


def generate_policy_summary(scenario: dict[str, Any], results: dict[str, Any], diagnostics: dict[str, Any]) -> dict[str, Any]:
    account_results = results.get("accounts", {}) if isinstance(results, dict) else {}
    ordered = sorted(account_results.items(), key=lambda item: abs(float(item[1])), reverse=True)
    winners = [account for account, value in ordered if float(value) > 0][:5]
    risks = _collect_warnings(diagnostics)
    return {
        "executive_summary": f"Signal compiled and ran the scenario '{scenario.get('scenario_name', 'selected scenario')}' using the available workbench pathway.",
        "expected_transmission_channel": explain_mechanism(scenario),
        "likely_winners": winners or ["Targeted accounts and linked suppliers, subject to SAM mapping."],
        "likely_risks": risks or ["No critical diagnostic warning was raised by the current screening checks."],
        "interpretation_caveat": "Current results use deterministic parsing and the Python SAM multiplier fallback unless a full CGE backend is configured.",
        "suggested_next_simulations": recommend_next_scenarios(scenario),
    }


def _collect_warnings(diagnostics: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for block in diagnostics.values() if isinstance(diagnostics, dict) else []:
        if isinstance(block, dict):
            warnings.extend(str(item) for item in block.get("warnings", []))
        elif isinstance(block, list):
            warnings.extend(str(item) for item in block)
    return list(dict.fromkeys(warnings))
