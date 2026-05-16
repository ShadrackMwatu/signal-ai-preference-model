"""Signal trajectory classification for Open Signals."""

from __future__ import annotations

from typing import Any

TRAJECTORY_LABELS = {"emerging", "strengthening", "persistent", "accelerating", "stabilizing", "weakening", "fading"}


def classify_signal_trajectory(signal: dict[str, Any], previous: dict[str, Any] | None = None) -> str:
    momentum = _norm(signal.get("momentum"))
    forecast = _norm(signal.get("forecast_direction") or signal.get("predicted_direction"))
    confidence = _num(signal.get("confidence_score"))
    adaptive = _num(signal.get("behavioral_intelligence_score") or signal.get("priority_score"))
    persistence = _num(signal.get("persistence_score"))
    source_confirmation = max(_num(signal.get("multi_source_confirmation_score")), _num(signal.get("cross_source_confirmation_score")))
    recurrence = _num(signal.get("historical_recurrence_score"))
    outcome = _norm(signal.get("outcome_learning_status"))
    rank_delta = _num(signal.get("ranking_movement"))
    previous_confidence = _num(previous.get("confidence_score")) if previous else 0.0
    confidence_delta = confidence - previous_confidence if previous else 0.0

    if "breakout" in momentum or rank_delta >= 4 or confidence_delta >= 12:
        return "accelerating"
    if "declin" in momentum or "fall" in forecast or confidence_delta <= -12:
        return "fading" if persistence < 35 else "weakening"
    if previous is None or _norm(signal.get("is_new_signal")) == "true":
        return "emerging"
    if "rising" in momentum or "rising" in forecast or rank_delta >= 2:
        return "strengthening"
    if persistence >= 70 or source_confirmation >= 70 or recurrence >= 70 or outcome == "historically_confirmed":
        return "persistent"
    return "stabilizing"


def enrich_signal_trajectories(signals: list[dict[str, Any]], previous_signals: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    previous_by_key = {_key(signal): signal for signal in previous_signals or []}
    previous_rank = {_key(signal): index for index, signal in enumerate(previous_signals or [])}
    enriched: list[dict[str, Any]] = []
    for index, signal in enumerate(signals or []):
        if not isinstance(signal, dict):
            continue
        item = dict(signal)
        key = _key(item)
        previous = previous_by_key.get(key)
        item["is_new_signal"] = previous is None
        item["ranking_movement"] = previous_rank.get(key, index) - index if previous_rank else 0
        item["trajectory_label"] = classify_signal_trajectory(item, previous)
        item["momentum"] = _momentum_from_trajectory(item.get("trajectory_label"), item.get("momentum"))
        if item["trajectory_label"] in {"accelerating", "strengthening", "emerging"}:
            item.setdefault("forecast_direction", "Rising")
        elif item["trajectory_label"] in {"weakening", "fading"}:
            item["forecast_direction"] = "Declining"
        else:
            item.setdefault("forecast_direction", "Stable")
        enriched.append(item)
    return enriched


def detect_emerging_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [signal for signal in signals if signal.get("trajectory_label") in {"emerging", "strengthening", "accelerating"}]


def detect_weakening_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [signal for signal in signals if signal.get("trajectory_label") in {"weakening", "fading"}]


def _momentum_from_trajectory(label: str, current: Any) -> str:
    if label == "accelerating":
        return "Breakout"
    if label in {"emerging", "strengthening"}:
        return "Rising"
    if label in {"weakening", "fading"}:
        return "Declining"
    return str(current or "Stable")


def _key(signal: dict[str, Any]) -> str:
    return " ".join(str(signal.get("signal_topic") or signal.get("topic") or signal.get("signal_cluster") or "").lower().split())


def _norm(value: Any) -> str:
    return " ".join(str(value or "").lower().split())


def _num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
