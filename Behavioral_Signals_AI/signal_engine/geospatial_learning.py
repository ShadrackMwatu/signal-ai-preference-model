"""Lightweight county-level aggregate geospatial learning."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.geography.county_matcher import enrich_signal_geography, geospatial_interpretation
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

MEMORY_PATH = Path("Behavioral_Signals_AI/outputs/geospatial_signal_memory.json")
DEFAULT_MEMORY = {"last_updated": None, "clusters": {}, "privacy_level": "county_level_aggregate_only"}


def load_geospatial_memory(path: str | Path | None = None) -> dict[str, Any]:
    payload = read_json(Path(path) if path else MEMORY_PATH, DEFAULT_MEMORY.copy())
    if not isinstance(payload, dict):
        return DEFAULT_MEMORY.copy()
    payload.setdefault("clusters", {})
    payload.setdefault("privacy_level", "county_level_aggregate_only")
    return payload


def update_geospatial_learning(signal: dict[str, Any], path: str | Path | None = None) -> dict[str, Any]:
    enriched = enrich_signal_geography(signal)
    memory_path = Path(path) if path else MEMORY_PATH
    memory = load_geospatial_memory(memory_path)
    key = _cluster_key(enriched)
    cluster = memory["clusters"].setdefault(key, {
        "county_code": enriched.get("county_code", ""),
        "county_name": enriched.get("county_name", "Kenya-wide"),
        "signal_cluster": enriched.get("semantic_cluster") or enriched.get("signal_topic", "aggregate signal"),
        "appearance_count": 0,
        "category_history": [],
        "urgency_history": [],
        "learned_pattern": "County-level aggregate evidence is still accumulating.",
    })
    cluster["appearance_count"] = int(cluster.get("appearance_count", 0)) + 1
    _append_unique(cluster["category_history"], str(enriched.get("signal_category", "other")), 10)
    _append_unique(cluster["urgency_history"], str(enriched.get("urgency", "Medium")), 10)
    if cluster["appearance_count"] >= 3:
        cluster["learned_pattern"] = f"Recurring aggregate signal pattern observed in {cluster.get('county_name', 'Kenya-wide')}."
        enriched["confidence_score"] = min(100.0, round(float(enriched.get("confidence_score", 50) or 50) + 4, 2))
        enriched["geospatial_recurrence"] = "recurring"
    else:
        enriched["geospatial_recurrence"] = "emerging"
    enriched["geospatial_insight"] = geospatial_interpretation(enriched)
    enriched["ml_rank_score"] = _ml_rank_score(enriched, cluster)
    memory["last_updated"] = datetime.now(UTC).isoformat()
    write_json(memory_path, memory)
    return enriched


def _cluster_key(signal: dict[str, Any]) -> str:
    county = signal.get("county_code") or signal.get("county_name") or "kenya-wide"
    cluster = signal.get("semantic_cluster") or signal.get("signal_topic") or "aggregate signal"
    return "|".join(str(part).lower().strip() for part in [county, cluster])


def _append_unique(items: list[str], value: str, limit: int) -> None:
    if value and value not in items:
        items.append(value)
    del items[:-limit]


def _ml_rank_score(signal: dict[str, Any], cluster: dict[str, Any]) -> float:
    confidence = float(signal.get("confidence_score", 50) or 50)
    priority = float(signal.get("priority_score", signal.get("behavioral_intelligence_score", 50)) or 50)
    recurrence = min(100.0, int(cluster.get("appearance_count", 0)) * 15.0)
    return round(min(100.0, confidence * 0.35 + priority * 0.40 + recurrence * 0.25), 2)