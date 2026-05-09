"""Summaries over Signal CGE simulation learning memory."""

from __future__ import annotations

from collections import Counter
from typing import Any

from signal_cge.learning.simulation_memory import load_simulation_memory


def summarize_learning_memory(limit: int = 50) -> dict[str, Any]:
    """Summarize recent simulation memory into model-learning signals."""

    events = load_simulation_memory(limit=limit)
    scenario_types = Counter(str(event.get("scenario_type") or "unknown") for event in events)
    targets = Counter(str(event.get("target_account") or "unknown") for event in events)
    warnings: Counter[str] = Counter()
    backends = Counter(str(event.get("backend_used") or "unknown") for event in events)
    patterns: Counter[str] = Counter()
    for event in events:
        diagnostics = event.get("diagnostics_summary", {})
        if isinstance(diagnostics, dict):
            for warning in diagnostics.get("warnings", []) or []:
                warnings[str(warning)] += 1
        interpretation = event.get("interpretation_summary", {})
        if isinstance(interpretation, dict):
            mechanism = interpretation.get("transmission_mechanism")
            if mechanism:
                patterns[str(mechanism)[:120]] += 1
    return {
        "event_count": len(events),
        "common_scenario_types": scenario_types.most_common(5),
        "common_target_accounts": targets.most_common(5),
        "repeated_warnings": warnings.most_common(5),
        "backend_limitations_observed": backends.most_common(5),
        "common_interpretation_patterns": patterns.most_common(5),
        "suggested_model_improvements": _suggestions(scenario_types, warnings, backends),
    }


def _suggestions(scenarios: Counter[str], warnings: Counter[str], backends: Counter[str]) -> list[str]:
    suggestions = []
    if scenarios.get("import_tariff") or scenarios.get("trade_policy"):
        suggestions.append("Expand trade-policy scenario templates and commodity account mappings.")
    if backends.get("python_sam_multiplier"):
        suggestions.append("Prioritize full equilibrium solver activation for price, trade balance, and revenue feedbacks.")
    if warnings:
        suggestions.append("Review repeated diagnostics and update calibration readiness checks.")
    return suggestions or ["Continue collecting lightweight simulation memory before proposing model changes."]
