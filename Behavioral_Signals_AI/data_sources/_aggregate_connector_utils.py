from __future__ import annotations

from datetime import UTC, datetime


def sample_record(topic: str, category: str, source_name: str, source_type: str, confidence: float, summary: str, reference: str = "") -> dict[str, object]:
    return {
        "topic": topic,
        "category": category,
        "source_name": source_name,
        "source_type": source_type,
        "location": "Kenya",
        "county_name": None,
        "county_code": None,
        "timestamp": datetime.now(UTC).isoformat(),
        "relative_interest": confidence,
        "observed_value": None,
        "unit": None,
        "confidence": confidence,
        "summary": summary,
        "privacy_level": "aggregate",
        "raw_reference": reference or source_name,
    }
