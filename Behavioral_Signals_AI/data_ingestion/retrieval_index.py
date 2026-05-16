"""Lightweight retrieval index for Open Signals aggregate intelligence."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.data_ingestion.privacy_filter import assert_no_private_fields
from Behavioral_Signals_AI.storage.storage_manager import read_json

OUTPUTS_DIR = Path("Behavioral_Signals_AI/outputs")
INDEX_SOURCES = {
    "ingested_signal_records": OUTPUTS_DIR / "ingested_signal_records.json",
    "latest_live_signals": OUTPUTS_DIR / "latest_live_signals.json",
    "historical_signal_memory": OUTPUTS_DIR / "historical_signal_memory.json",
    "outcome_learning_memory": OUTPUTS_DIR / "outcome_learning_memory.json",
    "geospatial_signal_memory": OUTPUTS_DIR / "geospatial_signal_memory.json",
    "behavioral_intelligence_memory": OUTPUTS_DIR / "behavioral_intelligence_memory.json",
}


def build_retrieval_index(paths: dict[str, str | Path] | None = None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for source_name, path in (paths or INDEX_SOURCES).items():
        data = read_json(path, {})
        for item in _extract_records(data):
            normalized = _to_index_record(item, source_name)
            if assert_no_private_fields(normalized):
                records.append(normalized)
    return records


def retrieve_relevant_context(query: str, location: str | None = None, category: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
    query_terms = _terms(query)
    scored: list[tuple[float, dict[str, Any]]] = []
    for record in build_retrieval_index():
        if location and location not in {"All", "Kenya", "Global"} and location.lower() not in str(record.get("location", "")).lower() and location.lower() not in str(record.get("county_name", "")).lower():
            continue
        if category and category != "All" and category.lower() not in str(record.get("category", "")).lower():
            continue
        score = _score_record(record, query_terms, location, category)
        if score > 0:
            scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:limit]]


def _extract_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ["records", "signals", "items", "memory", "clusters"]:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data] if data else []
    return []


def _to_index_record(item: dict[str, Any], source_name: str) -> dict[str, Any]:
    topic = item.get("topic") or item.get("signal_topic") or item.get("signal_cluster") or item.get("title") or "aggregate signal"
    return {
        "topic": str(topic),
        "category": str(item.get("category") or item.get("signal_category") or "other"),
        "source_name": str(item.get("source_name") or item.get("source_summary") or source_name),
        "source_type": str(item.get("source_type") or source_name),
        "location": str(item.get("location") or item.get("geographic_scope") or item.get("county_name") or "Kenya"),
        "county_name": item.get("county_name"),
        "county_code": item.get("county_code"),
        "timestamp": str(item.get("timestamp") or item.get("last_updated") or item.get("date") or ""),
        "relative_interest": item.get("relative_interest") or item.get("priority_score") or item.get("behavioral_intelligence_score"),
        "confidence": item.get("confidence") or item.get("confidence_score"),
        "summary": str(item.get("summary") or item.get("interpretation") or item.get("recommended_action") or topic),
        "privacy_level": "aggregate",
        "raw_reference": str(item.get("raw_reference") or item.get("source_url") or item.get("citation") or source_name),
    }


def _score_record(record: dict[str, Any], query_terms: set[str], location: str | None, category: str | None) -> float:
    blob = " ".join(str(value).lower() for value in record.values() if value)
    score = sum(2 for term in query_terms if term in blob)
    if location and location.lower() in blob:
        score += 3
    if category and category != "All" and category.lower() in blob:
        score += 3
    try:
        score += min(2.0, float(record.get("confidence") or 0) / 50.0)
    except (TypeError, ValueError):
        pass
    return score


def _terms(query: str) -> set[str]:
    return {term for term in re.findall(r"[a-zA-Z]{3,}", str(query or "").lower()) if term not in {"what", "show", "tell", "about", "signal", "signals"}}
