"""Retrieval tools for grounding Open Signals answers in aggregate memory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.data_ingestion.retrieval_index import retrieve_relevant_context
from Behavioral_Signals_AI.geography.county_matcher import signal_matches_location
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.storage.storage_manager import read_json
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display

OUTPUTS_DIR = Path("Behavioral_Signals_AI/outputs")

MEMORY_FILES = {
    "latest_live_signals": OUTPUTS_DIR / "latest_live_signals.json",
    "historical_signal_memory": OUTPUTS_DIR / "historical_signal_memory.json",
    "outcome_learning_memory": OUTPUTS_DIR / "outcome_learning_memory.json",
    "geospatial_signal_memory": OUTPUTS_DIR / "geospatial_signal_memory.json",
    "behavioral_intelligence_memory": OUTPUTS_DIR / "behavioral_intelligence_memory.json",
    "category_learning_memory": OUTPUTS_DIR / "category_learning_memory.json",
    "evaluation_metrics": OUTPUTS_DIR / "evaluation_metrics.json",
}


def retrieve_platform_context(location: str = "Kenya", category: str = "All", urgency: str = "All") -> dict[str, Any]:
    signals = retrieve_live_signals(location, category, urgency)
    return {
        "filters": {"location": location or "Kenya", "category": category or "All", "urgency": urgency or "All"},
        "signals": signals,
        "memory": retrieve_memory_context(signals),
    }


def retrieve_live_signals(location: str = "Kenya", category: str = "All", urgency: str = "All") -> list[dict[str, Any]]:
    payload = get_cached_or_fallback_signals()
    raw_signals = [signal for signal in payload.get("signals", []) if isinstance(signal, dict)]
    filtered: list[dict[str, Any]] = []
    for signal in raw_signals:
        if category and category != "All" and not category_matches_signal(signal, category):
            continue
        if urgency and urgency != "All" and str(signal.get("urgency", "")).lower() != urgency.lower():
            continue
        if location not in {"", "All", "Kenya", "Global"} and not signal_matches_location(signal, location):
            continue
        filtered.append(signal)
    return rank_signals_for_display(filtered or raw_signals)


def retrieve_memory_context(signals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    topics = {_normalize(signal.get("signal_topic", "")) for signal in list(signals or [])[:8]}
    memory = {name: read_json(path, _default_for_memory(name)) for name, path in MEMORY_FILES.items()}
    retrieval_query = " ".join(topic for topic in topics if topic)
    return {
        "retrieved_evidence": retrieve_relevant_context(retrieval_query, limit=8) if retrieval_query else retrieve_relevant_context("Kenya aggregate signals", limit=8),
        "historical": _select_relevant(memory["historical_signal_memory"], topics),
        "outcomes": _select_relevant(memory["outcome_learning_memory"], topics),
        "geospatial": _select_relevant(memory["geospatial_signal_memory"], topics),
        "behavioral": _select_relevant(memory["behavioral_intelligence_memory"], topics),
        "categories": _select_relevant(memory["category_learning_memory"], topics),
        "evaluation_metrics": memory["evaluation_metrics"] if isinstance(memory["evaluation_metrics"], dict) else {},
        "memory_files_available": {name: path.exists() for name, path in MEMORY_FILES.items()},
    }


def get_top_signal(location: str = "Kenya", category: str = "All", urgency: str = "All") -> dict[str, Any]:
    signals = retrieve_live_signals(location, category, urgency)
    return signals[0] if signals else {}


def compare_counties(county_a: str, county_b: str, category: str = "All", urgency: str = "All") -> dict[str, Any]:
    first = get_top_signal(county_a, category, urgency)
    second = get_top_signal(county_b, category, urgency)
    return {
        "county_a": county_a,
        "county_b": county_b,
        "county_a_signal": first,
        "county_b_signal": second,
        "stronger_county": county_a if _score(first) >= _score(second) else county_b,
    }


def explain_signal(topic: str, location: str = "Kenya") -> dict[str, Any]:
    normalized_topic = _normalize(topic)
    for signal in retrieve_live_signals(location):
        if normalized_topic and normalized_topic in _normalize(signal.get("signal_topic", "")):
            return signal
    return get_top_signal(location)


def summarize_opportunities(location: str = "Kenya") -> list[dict[str, Any]]:
    signals = retrieve_live_signals(location)
    return sorted(signals, key=lambda item: _score_field(item, "opportunity_intelligence_score", "opportunity_level"), reverse=True)[:5]


def summarize_risks(location: str = "Kenya") -> list[dict[str, Any]]:
    signals = retrieve_live_signals(location)
    return sorted(signals, key=lambda item: _score_field(item, "urgency_score", "urgency"), reverse=True)[:5]


def get_historical_pattern(topic_or_county: str) -> list[dict[str, Any]]:
    memory = retrieve_memory_context([])
    needle = _normalize(topic_or_county)
    matches: list[dict[str, Any]] = []
    for section in ["historical", "outcomes", "geospatial", "behavioral"]:
        for item in memory.get(section, []):
            if needle and needle in _normalize(str(item)):
                matches.append(item)
    return matches[:5]


def get_policy_implications(topic_or_county: str) -> list[str]:
    matches = get_historical_pattern(topic_or_county)
    implications = []
    for item in matches:
        note = item.get("policy_implication") or item.get("lesson_learned") or item.get("future_adjustment")
        if note:
            implications.append(str(note))
    return implications[:5]


def _default_for_memory(name: str) -> Any:
    return {} if name == "evaluation_metrics" else []


def _select_relevant(data: Any, topics: set[str]) -> list[dict[str, Any]]:
    records = _as_records(data)
    if not topics:
        return records[:8]
    selected = []
    for record in records:
        blob = _normalize(str(record))
        if any(topic and topic in blob for topic in topics):
            selected.append(record)
    return (selected or records)[:8]


def _as_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ["records", "signals", "clusters", "items", "memory"]:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data] if data else []
    return []


def _score(signal: dict[str, Any]) -> float:
    return max(
        _number(signal.get("priority_score")),
        _number(signal.get("behavioral_intelligence_score")),
        _number(signal.get("confidence_score")),
    )


def _score_field(signal: dict[str, Any], numeric_field: str, label_field: str) -> float:
    numeric = _number(signal.get(numeric_field))
    if numeric:
        return numeric
    labels = {"high": 80.0, "medium": 55.0, "moderate": 55.0, "low": 25.0}
    return labels.get(str(signal.get(label_field, "")).lower(), _score(signal))


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").lower().replace("_", " ").replace("-", " ").split())
