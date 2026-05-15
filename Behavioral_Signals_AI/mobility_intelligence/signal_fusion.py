"""Fuse aggregated place activity intelligence with live Behavioral Signals."""

from __future__ import annotations

from typing import Any


def fuse_mobility_with_live_signals(existing_signals: list[dict[str, Any]], mobility_signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not mobility_signals:
        return list(existing_signals or [])
    fused = [dict(signal) for signal in existing_signals or []]
    used_mobility: set[int] = set()
    for signal in fused:
        match_index, match = _best_match(signal, mobility_signals)
        if match is None:
            continue
        used_mobility.add(match_index)
        boost = min(12.0, float(match.get("demand_relevance", 0) or 0) / 10.0)
        signal["confidence_score"] = round(min(100.0, float(signal.get("confidence_score", 50) or 50) + boost), 2)
        signal["priority_score"] = round(min(100.0, float(signal.get("priority_score", 50) or 50) + boost), 2)
        signal["behavioral_intelligence_score"] = round(min(100.0, float(signal.get("behavioral_intelligence_score", signal.get("priority_score", 50)) or 50) + boost), 2)
        signal["place_activity_reinforced"] = True
        signal["place_activity_note"] = "Reinforced by aggregated place activity intelligence"
        signal["source_summary"] = _merge_source_summary(signal.get("source_summary"), match.get("source_summary"))
    for index, mobility in enumerate(mobility_signals):
        if index in used_mobility:
            continue
        fused.append(_new_signal_from_mobility(mobility))
    fused.sort(key=lambda item: (float(item.get("behavioral_intelligence_score", item.get("priority_score", 0)) or 0), float(item.get("confidence_score", 0) or 0)), reverse=True)
    return fused


def _best_match(signal: dict[str, Any], mobility_signals: list[dict[str, Any]]) -> tuple[int, dict[str, Any] | None]:
    category = str(signal.get("signal_category", "")).lower()
    topic = str(signal.get("signal_topic", "")).lower()
    for index, mobility in enumerate(mobility_signals):
        mob_category = str(mobility.get("signal_category", "")).lower()
        mob_topic = str(mobility.get("signal_topic", "")).lower()
        if category and category == mob_category:
            return index, mobility
        if category and category in mob_topic or mob_category and mob_category in topic:
            return index, mobility
    return -1, None


def _new_signal_from_mobility(mobility: dict[str, Any]) -> dict[str, Any]:
    score = float(mobility.get("demand_relevance", mobility.get("confidence_score", 55)) or 55)
    return {
        "signal_topic": mobility.get("signal_topic", "place activity demand signal"),
        "signal_category": mobility.get("signal_category", "other"),
        "demand_level": _level(score),
        "opportunity_level": _level(float(mobility.get("opportunity_score", score) or score)),
        "unmet_demand_likelihood": "Medium" if score >= 50 else "Low",
        "urgency": "High" if float(mobility.get("urgency_score", score) or score) >= 76 else "Medium" if score >= 50 else "Low",
        "geographic_scope": mobility.get("geographic_scope", "Kenya-wide"),
        "confidence_score": round(min(92.0, score), 2),
        "priority_score": round(score, 2),
        "behavioral_intelligence_score": round(score, 2),
        "momentum": mobility.get("momentum", "Stable"),
        "source_summary": mobility.get("source_summary", "Aggregated place activity intelligence"),
        "recommended_action": "Validate place-category demand with other aggregate signals and monitor category pressure.",
        "interpretation": mobility.get("interpretation", "Aggregated place intelligence suggests emerging demand."),
        "privacy_level": "aggregated_place_intelligence_only",
        "place_activity_reinforced": True,
        "place_activity_note": "Reinforced by aggregated place activity intelligence",
    }


def _merge_source_summary(left: object, right: object) -> str:
    parts = [str(item) for item in [left, right] if item]
    return " + ".join(dict.fromkeys(parts))


def _level(score: float) -> str:
    if score >= 74:
        return "High"
    if score >= 50:
        return "Moderate"
    return "Low"