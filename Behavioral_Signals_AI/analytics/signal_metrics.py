"""Core aggregate metrics for behavioral-economic signal interpretation."""

from __future__ import annotations

from typing import Any


def compute_signal_metrics(trend: dict[str, Any]) -> dict[str, float]:
    """Compute normalized aggregate signal metrics without individual-level data."""

    confidence = _percent(trend.get("confidence_score", trend.get("confidence", 0.55)))
    relevance = _percent(trend.get("relevance_to_demand", trend.get("aggregate_demand_score", 0.5)))
    volume = _volume_score(trend.get("volume") or trend.get("tweet_volume"))
    rank = _rank_score(trend.get("rank", 5))
    growth = _growth_score(trend.get("growth_indicator"))

    signal_strength = min(max((relevance * 0.34) + (confidence * 0.24) + (volume * 0.18) + (rank * 0.14) + (growth * 0.10), 1), 99)
    pressure = min(max((signal_strength * 0.56) + (_pressure_keyword_score(str(trend.get("trend_name", ""))) * 0.24) + (relevance * 0.20), 1), 99)
    persistence = min(max((signal_strength * 0.45) + (growth * 0.35) + (confidence * 0.20), 1), 99)
    volatility = min(max(100 - ((confidence * 0.55) + (rank * 0.25) + (persistence * 0.20)), 1), 99)

    return {
        "confidence": round(confidence, 1),
        "demand_relevance": round(relevance, 1),
        "volume_signal": round(volume, 1),
        "rank_signal": round(rank, 1),
        "growth_signal": round(growth, 1),
        "signal_strength": round(signal_strength, 1),
        "economic_pressure": round(pressure, 1),
        "persistence": round(persistence, 1),
        "volatility": round(volatility, 1),
    }


def _percent(value: Any) -> float:
    number = _number(value, 0.0)
    if 0 <= number <= 1:
        number *= 100
    return min(max(number, 0), 100)


def _volume_score(value: Any) -> float:
    volume = _number(value, None)
    if volume is None:
        return 45.0
    return min(max((volume / 250000.0) * 100.0, 8), 100)


def _rank_score(value: Any) -> float:
    rank = max(int(_number(value, 5) or 5), 1)
    return min(max(105 - (rank * 7), 10), 100)


def _growth_score(value: Any) -> float:
    text = str(value or "").lower()
    if "breakout" in text:
        return 95.0
    if "rising" in text or "up" in text or "+" in text:
        return 75.0
    if "declin" in text or "down" in text:
        return 25.0
    return 55.0


def _pressure_keyword_score(name: str) -> float:
    lowered = name.lower()
    keywords = ("shortage", "cost", "price", "fees", "access", "complaint", "water", "health", "fuel", "jobs")
    return 85.0 if any(keyword in lowered for keyword in keywords) else 45.0


def _number(value: Any, default: float | None) -> float | None:
    if value in {None, "", "not available"}:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace(",", "").replace("+", "").strip()
    multiplier = 1.0
    if cleaned.lower().endswith("k"):
        multiplier = 1000.0
        cleaned = cleaned[:-1]
    elif cleaned.lower().endswith("m"):
        multiplier = 1000000.0
        cleaned = cleaned[:-1]
    try:
        return float(cleaned) * multiplier
    except ValueError:
        return default