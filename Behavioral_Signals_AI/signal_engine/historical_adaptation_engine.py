"""Historical adaptation for Behavioral Signals AI scoring."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from Behavioral_Signals_AI.signal_engine.historical_memory import HISTORICAL_MEMORY_PATH, INSIGHT_INDEX_PATH, load_json

AFFORDABILITY_TERMS = {"maize", "unga", "food", "fuel", "rent", "prices", "transport", "fees"}
STRESS_CATEGORIES = {"food and agriculture", "cost of living", "health", "jobs and labour market", "water and sanitation", "security and governance"}


def apply_historical_adaptation(signal: dict[str, Any]) -> dict[str, Any]:
    matches = find_similar_historical_episodes(signal)
    index = load_json(INSIGHT_INDEX_PATH, {"themes": {}, "counties": {}, "categories": {}, "lessons": []})
    adjustment = _historical_adjustment(signal, matches, index)
    adapted = dict(signal)
    if adjustment:
        adapted["confidence_score"] = round(min(100.0, max(0.0, _num(adapted.get("confidence_score"), 50) + adjustment)), 1)
        adapted["demand_intelligence_score"] = round(min(100.0, max(0.0, _num(adapted.get("demand_intelligence_score"), 50) + adjustment * 0.7)), 1)
        adapted["opportunity_intelligence_score"] = round(min(100.0, max(0.0, _num(adapted.get("opportunity_intelligence_score"), 50) + adjustment * 0.5)), 1)
    adapted["historical_pattern_match"] = _pattern_label(signal, matches)
    adapted["historical_reliability_adjustment"] = round(adjustment, 2)
    adapted["historical_lesson_used"] = _lesson(signal, matches, index)
    adapted["seasonal_recurrence"] = _seasonal_recurrence(signal, matches)
    adapted["county_recurrence"] = _county_recurrence(signal, matches)
    return adapted


def find_similar_historical_episodes(signal: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    payload = load_json(HISTORICAL_MEMORY_PATH, {"records": []})
    records = payload.get("records", []) if isinstance(payload, dict) else []
    topic = str(signal.get("signal_topic", ""))
    cluster = str(signal.get("semantic_cluster") or topic)
    category = str(signal.get("signal_category", ""))
    scope = str(signal.get("geographic_scope", ""))
    scored: list[tuple[float, dict[str, Any]]] = []
    for record in records:
        score = 0.0
        score += SequenceMatcher(None, topic.lower(), str(record.get("signal_topic", "")).lower()).ratio() * 0.36
        score += SequenceMatcher(None, cluster.lower(), str(record.get("signal_cluster", "")).lower()).ratio() * 0.30
        if category and category == record.get("category"):
            score += 0.20
        if scope and scope == record.get("county_or_scope"):
            score += 0.14
        if score >= 0.48:
            scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:limit]]


def _historical_adjustment(signal: dict[str, Any], matches: list[dict[str, Any]], index: dict[str, Any]) -> float:
    if not matches:
        return 0.0
    category = str(signal.get("signal_category", ""))
    topic_text = str(signal.get("signal_topic", "")).lower()
    high_relevance = sum(1 for record in matches if record.get("future_relevance") == "High")
    false_positive_like = sum(1 for record in matches if record.get("validation_status") == "unvalidated" and float(record.get("confidence_score", 0)) < 45)
    recurring_category = int(index.get("categories", {}).get(category, 0))
    adjustment = high_relevance * 2.5 + min(6.0, recurring_category * 0.25) - false_positive_like * 2.0
    if any(term in topic_text for term in AFFORDABILITY_TERMS):
        adjustment += 2.0
    if category in STRESS_CATEGORIES:
        adjustment += 1.5
    return max(-8.0, min(12.0, adjustment))


def _pattern_label(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    if not matches:
        return "No close historical pattern yet"
    top = matches[0]
    return f"Similar to prior {top.get('category', 'aggregate')} signal on {top.get('date', 'a past date')}"


def _lesson(signal: dict[str, Any], matches: list[dict[str, Any]], index: dict[str, Any]) -> str:
    if matches:
        high = [record for record in matches if record.get("future_relevance") == "High"]
        if high:
            return "Similar past signals became important when confidence, urgency, and source agreement rose together."
        return "Historical memory suggests monitoring persistence before strengthening action recommendations."
    lessons = index.get("lessons", []) if isinstance(index, dict) else []
    if lessons:
        return str(lessons[-1])
    return "No historical lesson is strong yet; the system is accumulating institutional memory."


def _seasonal_recurrence(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    if len(matches) >= 3:
        return "Moderate"
    if matches:
        return "Low"
    return "None detected"


def _county_recurrence(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    scope = signal.get("geographic_scope")
    if scope == "Kenya-wide":
        return "Kenya-wide pattern"
    repeated = sum(1 for record in matches if record.get("county_or_scope") == scope)
    if repeated >= 2:
        return "Recurring county pattern"
    return "No strong county recurrence yet"


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
