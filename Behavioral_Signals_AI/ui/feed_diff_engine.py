"""Diff and ranking helpers for the Behavioral Signals AI live feed."""

from __future__ import annotations

from typing import Any

_CONFIDENCE_DELTA_THRESHOLD = 5.0


def has_material_signal_change(previous_signals: list[dict[str, Any]] | None, current_signals: list[dict[str, Any]] | None) -> bool:
    """Return true only when the visible feed needs a new render."""
    previous = _normalize(previous_signals or [])
    current = _normalize(current_signals or [])
    if not previous and not current:
        return False
    if bool(previous) != bool(current):
        return True

    previous_keys = [_signal_key(signal) for signal in previous]
    current_keys = [_signal_key(signal) for signal in current]
    if set(previous_keys) != set(current_keys):
        return True
    if previous_keys[:5] != current_keys[:5]:
        return True

    previous_by_key = {_signal_key(signal): signal for signal in previous}
    for signal in current:
        key = _signal_key(signal)
        old = previous_by_key.get(key)
        if old is None:
            return True
        if _changed_label(old, signal, "urgency"):
            return True
        if _changed_label(old, signal, "momentum"):
            return True
        if _changed_label(old, signal, "forecast_direction") or _changed_label(old, signal, "predicted_direction"):
            return True
        if abs(_number(signal.get("confidence_score")) - _number(old.get("confidence_score"))) > _CONFIDENCE_DELTA_THRESHOLD:
            return True
    return False


def rank_signals_for_display(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank by collective intelligence so stronger emerging issues rise smoothly."""
    return sorted(signals or [], key=_ranking_score, reverse=True)


def signal_signature(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return compact fields used for render-cache comparison."""
    return [
        {
            "key": _signal_key(signal),
            "urgency": str(signal.get("urgency", "")),
            "momentum": str(signal.get("momentum", "")),
            "forecast_direction": str(signal.get("forecast_direction") or signal.get("predicted_direction") or ""),
            "confidence_score": round(_number(signal.get("confidence_score")), 2),
            "ranking_score": round(_ranking_score(signal), 2),
        }
        for signal in _normalize(signals)
    ]


def _normalize(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(signal) for signal in signals if isinstance(signal, dict)]


def _signal_key(signal: dict[str, Any]) -> str:
    key = signal.get("semantic_cluster") or signal.get("signal_cluster") or signal.get("signal_topic") or signal.get("topic") or ""
    return " ".join(str(key).lower().strip().split())


def _changed_label(previous: dict[str, Any], current: dict[str, Any], field: str) -> bool:
    return str(previous.get(field, "")).lower() != str(current.get(field, "")).lower()


def _ranking_score(signal: dict[str, Any]) -> float:
    urgency = {"high": 100.0, "medium": 62.0, "low": 35.0}.get(str(signal.get("urgency", "")).lower(), _number(signal.get("urgency_score"), 50))
    momentum = {"breakout": 100.0, "rising": 82.0, "stable": 55.0, "declining": 28.0}.get(str(signal.get("momentum", "")).lower(), 50.0)
    forecast = 78.0 if str(signal.get("forecast_direction") or signal.get("predicted_direction", "")).lower() == "rising" else 50.0
    outcome = _number(signal.get("historical_accuracy_score"), 50)
    return (
        _number(signal.get("behavioral_intelligence_score"), _number(signal.get("priority_score"), 50)) * 0.20
        + _number(signal.get("persistence_score"), 50) * 0.13
        + _number(signal.get("multi_source_confirmation_score"), _number(signal.get("cross_source_confirmation_score"), 50)) * 0.13
        + _number(signal.get("geographic_spread_score"), 50) * 0.10
        + momentum * 0.12
        + _number(signal.get("historical_recurrence_score"), 50) * 0.10
        + outcome * 0.07
        + urgency * 0.08
        + _number(signal.get("confidence_score"), 50) * 0.05
        + forecast * 0.02
    )


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)