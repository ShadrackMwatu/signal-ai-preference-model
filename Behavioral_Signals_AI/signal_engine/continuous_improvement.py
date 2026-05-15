"""Continuous improvement helpers for Behavioral Signals AI ranking behavior."""

from __future__ import annotations

from collections import Counter
from typing import Any


def improve_after_refresh(signals: list[dict[str, Any]], memory: dict[str, Any]) -> dict[str, Any]:
    clusters = memory.get("clusters", {})
    categories = Counter(signal.get("signal_category", "other") for signal in signals)
    recurring = [cluster.get("topic") for cluster in clusters.values() if int(cluster.get("number_of_appearances", 0)) >= 3]
    false_positive_candidates = [signal.get("signal_topic") for signal in signals if signal.get("validation_status") == "unvalidated" and float(signal.get("confidence_score", 0)) < 45]
    source_reliability_updates = _source_reliability_updates(signals)
    return {
        "source_reliability_updates": source_reliability_updates,
        "category_mapping_observations": dict(categories),
        "known_kenya_topic_clusters": recurring[-20:],
        "false_positive_candidates": false_positive_candidates,
        "recurring_validated_signals": [signal.get("signal_topic") for signal in signals if signal.get("validation_status") == "validated"],
        "ranking_note": "Future ranking favors persistent, validated, multi-source, Kenya-relevant signals and down-ranks noisy or rejected signals.",
    }


def _source_reliability_updates(signals: list[dict[str, Any]]) -> dict[str, float]:
    scores: dict[str, list[float]] = {}
    for signal in signals:
        source = str(signal.get("source_summary", "Aggregate public sources"))
        scores.setdefault(source, []).append(float(signal.get("accuracy_confidence", 50)))
    return {source: round(sum(values) / len(values), 2) for source, values in scores.items() if values}