"""Adaptive refresh interval selection for Open Signals runtime."""

from __future__ import annotations

from typing import Any

FAST_TOPICS = ["fuel", "price", "prices", "labor unrest", "labour unrest", "strike", "breaking", "shortage"]
SLOW_TOPICS = ["drought", "seasonal", "climate", "agriculture cycle"]


def adaptive_refresh_seconds(signals: list[dict[str, Any]], default_seconds: int = 300) -> int:
    if not signals:
        return default_seconds
    fastest = default_seconds
    for signal in signals:
        fastest = min(fastest, refresh_interval_for_signal(signal, default_seconds))
    return max(30, fastest)


def refresh_interval_for_signal(signal: dict[str, Any], default_seconds: int = 300) -> int:
    topic = str(signal.get("signal_topic") or signal.get("topic") or "").lower()
    trajectory = str(signal.get("trajectory_label") or "").lower()
    urgency = str(signal.get("urgency") or "").lower()
    volatility = _num(signal.get("volatility_score"))
    if trajectory in {"accelerating", "strengthening"} or urgency == "high" or volatility >= 75 or any(term in topic for term in FAST_TOPICS):
        return 60
    if trajectory in {"persistent", "stabilizing"} and any(term in topic for term in SLOW_TOPICS):
        return 900
    if trajectory in {"fading", "weakening"}:
        return 600
    return default_seconds


def _num(value) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
