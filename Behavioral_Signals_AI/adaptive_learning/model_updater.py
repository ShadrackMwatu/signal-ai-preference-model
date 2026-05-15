"""Adaptive model updater for rule-based Behavioral Signals weights."""

from __future__ import annotations

from typing import Any

from .online_calibrator import DEFAULT_WEIGHTS


def update_adaptive_weights(records: list[dict[str, Any]]) -> dict[str, float]:
    """Adjust weights conservatively from aggregate accuracy history."""

    weights = dict(DEFAULT_WEIGHTS)
    accurate = [row for row in records if row.get("accuracy_result") == "accurate"]
    missed = [row for row in records if row.get("accuracy_result") == "missed"]
    if len(accurate) > len(missed):
        weights["historical_accuracy"] = min(weights["historical_accuracy"] + 0.03, 0.24)
        weights["signal_persistence"] = min(weights["signal_persistence"] + 0.02, 0.24)
    elif len(missed) > len(accurate):
        weights["volatility_penalty"] = 0.08
        weights["trend_growth"] = max(weights["trend_growth"] - 0.02, 0.08)
    return weights


def suggest_model_updates(records: list[dict[str, Any]]) -> list[str]:
    suggestions = []
    if not records:
        return ["Collect live aggregate prediction snapshots before adapting weights."]
    if sum(1 for row in records if row.get("accuracy_result") == "missed"):
        suggestions.append("Review volatile categories and reduce high-demand predictions for short-lived signals.")
    if len({row.get("source") for row in records if row.get("source")}) < 2:
        suggestions.append("Increase cross-provider confirmation by enabling search, social, and news providers.")
    return suggestions or ["Current adaptive weighting is stable for available aggregate history."]