"""Validation layer for Kenya aggregate signals against trusted reference classes."""

from __future__ import annotations

from typing import Any

TRUSTED_CATEGORY_SOURCES = {
    "food and agriculture": ["food price data", "Kilimostat", "WFP", "World Bank"],
    "cost of living": ["KNBS", "CBK", "public news frequency"],
    "energy": ["CBK", "public news frequency"],
    "finance and credit": ["CBK", "public news frequency"],
    "jobs and labour market": ["KNBS", "public news frequency"],
}


def validate_signal(signal: dict[str, Any]) -> dict[str, Any]:
    category = str(signal.get("signal_category", "other"))
    source_summary = str(signal.get("source_summary", "")).lower()
    trusted_sources = TRUSTED_CATEGORY_SOURCES.get(category, ["public news frequency", "historical trend behavior"])
    matched = [source for source in trusted_sources if source.lower() in source_summary]
    if matched:
        status = "validated"
        confidence = 82
        notes = "Signal aligns with a trusted reference source class."
    elif any(term in source_summary for term in ["news", "search", "public", "official", "price"]):
        status = "partially_validated"
        confidence = 66
        notes = "Signal is supported by public aggregate evidence but needs additional official confirmation."
    else:
        status = "unvalidated"
        confidence = 48
        notes = "Signal is currently based on limited aggregate evidence."
    return {
        "validation_status": status,
        "validation_sources": matched or trusted_sources[:2],
        "validation_notes": notes,
        "accuracy_confidence": confidence,
    }