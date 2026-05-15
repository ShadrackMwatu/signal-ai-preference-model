"""Adaptive learning engine for Kenya aggregate signal intelligence."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

MEMORY_PATH = Path(os.getenv("SIGNAL_CLUSTER_MEMORY_PATH", "Behavioral_Signals_AI/outputs/signal_memory.json"))
FEEDBACK_PATH = Path(os.getenv("SIGNAL_FEEDBACK_PATH", "Behavioral_Signals_AI/outputs/signal_feedback.json"))


def load_cluster_memory(path: str | Path | None = None) -> dict[str, Any]:
    data = read_json(Path(path or MEMORY_PATH), {"clusters": {}, "last_updated": None})
    return data if isinstance(data, dict) else {"clusters": {}, "last_updated": None}


def save_cluster_memory(memory: dict[str, Any], path: str | Path | None = None) -> None:
    write_json(Path(path or MEMORY_PATH), memory)


def load_feedback(path: str | Path | None = None) -> dict[str, Any]:
    data = read_json(Path(path or FEEDBACK_PATH), {"feedback": []})
    return data if isinstance(data, dict) else {"feedback": []}


def save_feedback(feedback: dict[str, Any], path: str | Path | None = None) -> None:
    write_json(Path(path or FEEDBACK_PATH), feedback)


def analyst_confirms_signal(topic: str, note: str = "") -> dict[str, Any]:
    return _append_feedback("confirm", topic, note=note)


def analyst_rejects_signal(topic: str, note: str = "") -> dict[str, Any]:
    return _append_feedback("reject", topic, note=note)


def analyst_corrects_category(topic: str, category: str, note: str = "") -> dict[str, Any]:
    return _append_feedback("correct_category", topic, category=category, note=note)


def analyst_corrects_county(topic: str, county: str, note: str = "") -> dict[str, Any]:
    return _append_feedback("correct_county", topic, county=county, note=note)


def analyst_updates_interpretation(topic: str, interpretation: str, note: str = "") -> dict[str, Any]:
    return _append_feedback("update_interpretation", topic, interpretation=interpretation, note=note)


def adapt_signal_scores(signal: dict[str, Any], memory: dict[str, Any] | None = None, feedback: dict[str, Any] | None = None) -> dict[str, Any]:
    mem = memory or load_cluster_memory()
    fb = feedback or load_feedback()
    cluster_key = find_cluster_key(str(signal.get("signal_topic", "")), mem)
    cluster = mem.get("clusters", {}).get(cluster_key, {}) if cluster_key else {}
    appearances = int(cluster.get("number_of_appearances", 0))
    persistence = min(100.0, 35.0 + appearances * 13.0)
    source_agreement = float(signal.get("multi_source_confirmation_score", 45))
    recency = float(signal.get("recency_score", 65))
    category_confidence = float(signal.get("category_confidence_score", 55))
    county_specificity = 72.0 if str(signal.get("geographic_scope", "Kenya-wide")) != "Kenya-wide" else 55.0
    validation = float(signal.get("accuracy_confidence", 50))
    reliability = float(signal.get("source_reliability_score", 58))
    momentum_score = _momentum_score(str(signal.get("momentum", "Stable")))
    volatility = _volatility_penalty(cluster)
    feedback_adjustment = _feedback_adjustment(str(signal.get("signal_topic", "")), fb, signal)
    confidence = (
        persistence * 0.16
        + source_agreement * 0.15
        + recency * 0.10
        + category_confidence * 0.12
        + county_specificity * 0.08
        + validation * 0.15
        + reliability * 0.12
        + momentum_score * 0.08
        + (100 - volatility) * 0.04
        + feedback_adjustment
    )
    confidence = max(0.0, min(100.0, confidence))
    demand = max(0.0, min(100.0, float(signal.get("priority_score", 50)) * 0.45 + confidence * 0.35 + persistence * 0.20))
    opportunity = max(0.0, min(100.0, float(signal.get("priority_score", 50)) * 0.40 + confidence * 0.30 + source_agreement * 0.20 + validation * 0.10))
    urgency = max(0.0, min(100.0, _urgency_base(signal) * 0.55 + momentum_score * 0.25 + persistence * 0.20))
    signal.update(
        {
            "confidence_score": round(confidence, 1),
            "demand_intelligence_score": round(demand, 1),
            "opportunity_intelligence_score": round(opportunity, 1),
            "urgency_score": round(urgency, 1),
            "score_explanation": (
                "Score combines persistence, source agreement, recency, category confidence, county specificity, "
                "validation evidence, source reliability, analyst feedback, momentum, and volatility."
            ),
            "persistence_badge": "Persistent" if persistence >= 60 else "Emerging",
        }
    )
    if feedback_adjustment < -8:
        signal["confidence_score"] = max(0, round(signal["confidence_score"] - 10, 1))
    return signal


def update_signal_memory(signals: list[dict[str, Any]], path: str | Path | None = None) -> dict[str, Any]:
    memory = load_cluster_memory(path)
    clusters = memory.setdefault("clusters", {})
    now = datetime.now(UTC).isoformat()
    for signal in signals:
        topic = str(signal.get("signal_topic", ""))
        key = find_cluster_key(topic, memory) or _cluster_key(topic)
        cluster = clusters.setdefault(
            key,
            {
                "topic": topic,
                "first_seen": now,
                "number_of_appearances": 0,
                "source_history": [],
                "category_history": [],
                "county_history": [],
                "confidence_history": [],
                "urgency_history": [],
                "momentum_history": [],
                "interpretation_history": [],
            },
        )
        cluster["last_seen"] = now
        cluster["number_of_appearances"] = int(cluster.get("number_of_appearances", 0)) + 1
        _append_limited(cluster, "source_history", signal.get("source_summary"))
        _append_limited(cluster, "category_history", signal.get("signal_category"))
        _append_limited(cluster, "county_history", signal.get("geographic_scope"))
        _append_limited(cluster, "confidence_history", signal.get("confidence_score"))
        _append_limited(cluster, "urgency_history", signal.get("urgency"))
        _append_limited(cluster, "momentum_history", signal.get("momentum"))
        _append_limited(cluster, "interpretation_history", signal.get("interpretation"))
    memory["last_updated"] = now
    save_cluster_memory(memory, path)
    return memory


def find_cluster_key(topic: str, memory: dict[str, Any]) -> str | None:
    key = _cluster_key(topic)
    clusters = memory.get("clusters", {})
    if key in clusters:
        return key
    for existing_key, cluster in clusters.items():
        existing_topic = str(cluster.get("topic", existing_key))
        if SequenceMatcher(None, topic.lower(), existing_topic.lower()).ratio() > 0.78:
            return existing_key
    return None


def _append_feedback(action: str, topic: str, **kwargs: Any) -> dict[str, Any]:
    payload = load_feedback()
    event = {"timestamp": datetime.now(UTC).isoformat(), "action": action, "topic": topic, **kwargs}
    payload.setdefault("feedback", []).append(event)
    save_feedback(payload)
    return event


def _feedback_adjustment(topic: str, feedback: dict[str, Any], signal: dict[str, Any]) -> float:
    adjustment = 0.0
    for event in feedback.get("feedback", []):
        if SequenceMatcher(None, topic.lower(), str(event.get("topic", "")).lower()).ratio() <= 0.78:
            continue
        action = event.get("action")
        if action == "confirm":
            adjustment += 8
        elif action == "reject":
            adjustment -= 20
        elif action == "correct_category" and event.get("category"):
            signal["signal_category"] = event["category"]
            adjustment += 4
        elif action == "correct_county" and event.get("county"):
            signal["geographic_scope"] = event["county"]
            adjustment += 4
        elif action == "update_interpretation" and event.get("interpretation"):
            signal["interpretation"] = event["interpretation"]
            adjustment += 3
    return max(-30, min(25, adjustment))


def _cluster_key(topic: str) -> str:
    return " ".join(topic.lower().strip().split())[:120]


def _append_limited(cluster: dict[str, Any], key: str, value: Any, limit: int = 25) -> None:
    if value in {None, ""}:
        return
    values = list(cluster.get(key, []))
    values.append(value)
    cluster[key] = values[-limit:]


def _momentum_score(momentum: str) -> float:
    return {"Breakout": 92, "Rising": 74, "Stable": 55, "Declining": 32}.get(momentum, 50)


def _urgency_base(signal: dict[str, Any]) -> float:
    return {"High": 85, "Medium": 58, "Low": 30}.get(str(signal.get("urgency", "Medium")), 55)


def _volatility_penalty(cluster: dict[str, Any]) -> float:
    momentum = list(cluster.get("momentum_history", []))[-6:]
    return 45.0 if len(set(momentum)) >= 3 else 15.0


