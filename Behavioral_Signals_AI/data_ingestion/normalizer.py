"""Normalize public/aggregate source records into the Open Signals ingestion schema."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

REQUIRED_FIELDS = [
    "topic", "category", "source_name", "source_type", "location", "county_name", "county_code",
    "timestamp", "relative_interest", "observed_value", "unit", "confidence", "summary",
    "privacy_level", "raw_reference",
]


def normalize_record(record: dict[str, Any], source: dict[str, Any] | None = None) -> dict[str, Any]:
    source = source or {}
    topic = str(record.get("topic") or record.get("signal_topic") or record.get("title") or source.get("source_name") or "aggregate signal")
    normalized = {
        "topic": topic[:180],
        "category": str(record.get("category") or record.get("signal_category") or _category_from_topic(topic)),
        "source_name": str(record.get("source_name") or source.get("source_name") or source.get("name") or "unknown_source"),
        "source_type": str(record.get("source_type") or source.get("source_type") or "official_statistics"),
        "location": str(record.get("location") or "Kenya"),
        "county_name": record.get("county_name"),
        "county_code": record.get("county_code"),
        "timestamp": str(record.get("timestamp") or datetime.now(UTC).isoformat()),
        "relative_interest": _bounded(record.get("relative_interest"), 55),
        "observed_value": record.get("observed_value"),
        "unit": record.get("unit"),
        "confidence": _bounded(record.get("confidence"), source.get("reliability_prior", 60)),
        "summary": str(record.get("summary") or record.get("interpretation") or topic)[:500],
        "privacy_level": "aggregate",
        "raw_reference": str(record.get("raw_reference") or record.get("source_url") or record.get("citation") or source.get("source_name") or "")[:300],
    }
    return normalized


def validate_normalized_record(record: dict[str, Any]) -> bool:
    return all(field in record for field in REQUIRED_FIELDS) and record.get("privacy_level") == "aggregate"


def _bounded(value: Any, default: Any) -> float:
    try:
        number = float(value if value is not None else default)
    except (TypeError, ValueError):
        number = float(default or 0)
    return max(0.0, min(100.0, number))


def _category_from_topic(topic: str) -> str:
    text = topic.lower()
    if any(term in text for term in ["maize", "food", "fertilizer", "farm", "agriculture"]):
        return "food and agriculture"
    if any(term in text for term in ["inflation", "prices", "cost", "affordability"]):
        return "cost of living"
    if any(term in text for term in ["credit", "loan", "interest", "exchange", "bank"]):
        return "finance"
    if any(term in text for term in ["water", "rain", "drought", "climate"]):
        return "climate and environment"
    if any(term in text for term in ["jobs", "labour", "employment"]):
        return "jobs and labour market"
    return "other"
