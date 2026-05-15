"""Source learning for Behavioral Signals AI aggregate providers."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

SOURCE_LEARNING_PATH = Path(os.getenv("SIGNAL_SOURCE_LEARNING_PATH", "Behavioral_Signals_AI/outputs/source_learning.json"))
DEFAULT_SOURCE_LEARNING = {"sources": {}, "underrepresented_counties": [], "predictive_topics": {}, "last_updated": None}


def load_source_learning(path: str | Path | None = None) -> dict[str, Any]:
    data = read_json(Path(path or SOURCE_LEARNING_PATH), DEFAULT_SOURCE_LEARNING.copy())
    return data if isinstance(data, dict) else DEFAULT_SOURCE_LEARNING.copy()


def save_source_learning(payload: dict[str, Any], path: str | Path | None = None) -> None:
    write_json(Path(path or SOURCE_LEARNING_PATH), payload)


def update_source_learning(signals: list[dict[str, Any]], path: str | Path | None = None) -> dict[str, Any]:
    learning = load_source_learning(path)
    sources = learning.setdefault("sources", {})
    predictive_topics = learning.setdefault("predictive_topics", {})
    counties_seen: set[str] = set()
    for signal in signals:
        source = str(signal.get("source_summary", "Aggregate public sources"))[:160]
        source_entry = sources.setdefault(source, {"observations": 0, "average_accuracy": 0.0, "noise_observations": 0})
        observations = int(source_entry.get("observations", 0)) + 1
        accuracy = _num(signal.get("accuracy_confidence"), _num(signal.get("confidence_score"), 50))
        previous = _num(source_entry.get("average_accuracy"), accuracy)
        source_entry["observations"] = observations
        source_entry["average_accuracy"] = round(((previous * (observations - 1)) + accuracy) / observations, 2)
        if _num(signal.get("noise_level"), 0) > 55:
            source_entry["noise_observations"] = int(source_entry.get("noise_observations", 0)) + 1
        topic = str(signal.get("semantic_cluster") or signal.get("signal_topic", "Kenya signal"))[:140]
        topic_entry = predictive_topics.setdefault(topic, {"appearances": 0, "directions": [], "categories": []})
        topic_entry["appearances"] = int(topic_entry.get("appearances", 0)) + 1
        _append_limited(topic_entry, "directions", signal.get("predicted_direction"))
        _append_limited(topic_entry, "categories", signal.get("signal_category"))
        scope = str(signal.get("geographic_scope", "Kenya-wide"))
        if scope != "Kenya-wide":
            counties_seen.add(scope)
    learning["underrepresented_counties"] = _underrepresented_counties(counties_seen)
    learning["last_updated"] = datetime.now(UTC).isoformat()
    save_source_learning(learning, path)
    return learning


def _append_limited(payload: dict[str, Any], key: str, value: Any, limit: int = 20) -> None:
    if value in {None, ""}:
        return
    values = list(payload.get(key, []))
    values.append(value)
    payload[key] = values[-limit:]


def _underrepresented_counties(counties_seen: set[str]) -> list[str]:
    priority = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu", "Machakos", "Turkana", "Garissa"]
    return [county for county in priority if county not in counties_seen]


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
