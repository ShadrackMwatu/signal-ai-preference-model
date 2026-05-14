"""Deterministic classification helpers for aggregate trend intelligence."""

from __future__ import annotations

from typing import Any

from .trend_normalizer import build_implication, classify_category


def classify_trend(record: dict[str, Any]) -> dict[str, Any]:
    """Add category, demand relevance, and implication fields when missing."""

    enriched = dict(record)
    category = str(enriched.get("category") or classify_category(str(enriched.get("trend_name", ""))))
    confidence = float(enriched.get("confidence", 0.55) or 0.55)
    volume = enriched.get("volume") or enriched.get("tweet_volume")
    volume_score = 0.45
    if isinstance(volume, (int, float)):
        volume_score = min(float(volume) / 200000.0, 1.0)
    relevance = float(enriched.get("relevance_to_demand", 0.0) or 0.0)
    if relevance <= 0:
        relevance = min((confidence * 0.55) + (volume_score * 0.25) + (0.15 if category != "general_public_interest" else 0.05), 0.98)
    enriched["category"] = category
    enriched["confidence"] = round(confidence, 3)
    enriched["relevance_to_demand"] = round(relevance, 3)
    enriched["possible_policy_or_business_implication"] = enriched.get("possible_policy_or_business_implication") or build_implication(
        str(enriched.get("trend_name", "Trend")), category, relevance
    )
    return enriched


def classify_trend_batch(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [classify_trend(record) for record in records]