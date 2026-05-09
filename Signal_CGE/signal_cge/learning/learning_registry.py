"""Summaries over Signal CGE simulation learning memory."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from .simulation_memory import load_simulation_memory


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


def write_learning_summary(limit: int = 100) -> dict[str, Any]:
    """Write a lightweight repo-runtime learning summary."""

    summary = summarize_learning_memory(limit=limit)
    output_dir = Path("Signal_CGE") / "outputs" / "learning_summaries"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"learning_summary_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return {"path": str(path), "summary": summary}


def _suggestions(scenarios: Counter[str], warnings: Counter[str], backends: Counter[str]) -> list[str]:
    suggestions = []
    if scenarios.get("import_tariff") or scenarios.get("trade_policy"):
        suggestions.append("Expand trade-policy scenario templates and commodity account mappings.")
    if backends.get("python_sam_multiplier"):
        suggestions.append("Prioritize full equilibrium solver activation for price, trade balance, and revenue feedbacks.")
    if warnings:
        suggestions.append("Review repeated diagnostics and update calibration readiness checks.")
    return suggestions or ["Continue collecting lightweight simulation memory before proposing model changes."]
