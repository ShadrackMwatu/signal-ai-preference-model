"""Diff, ranking, and render-cache helpers for the Behavioral Signals AI live feed."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

_CONFIDENCE_DELTA_THRESHOLD = 5.0
_ADAPTIVE_DELTA_THRESHOLD = 5.0


def render_cache_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return Path(os.getenv("SIGNAL_RENDER_CACHE", "Behavioral_Signals_AI/outputs/render_cache.json"))


def default_render_cache() -> dict[str, Any]:
    return {
        "last_signal_signature": [],
        "live_feed_html": "",
        "emerging_signals_html": "",
        "interpretation_markdown": "",
        "historical_learning_markdown": "",
        "last_rendered_at": None,
        "views": {},
    }


def load_render_cache(path: str | Path | None = None) -> dict[str, Any]:
    cache = read_json(render_cache_path(path), default_render_cache())
    if not isinstance(cache, dict):
        return default_render_cache()
    base = default_render_cache()
    base.update(cache)
    base.setdefault("views", {})
    return base


def get_cached_rendered_outputs(cache_key: str, current_signature: list[dict[str, Any]], path: str | Path | None = None) -> tuple[str, str, str, str] | None:
    cache = load_render_cache(path)
    view = cache.get("views", {}).get(cache_key)
    if not isinstance(view, dict):
        return None
    cached_signature = view.get("last_signal_signature", [])
    if has_material_signal_change(cached_signature, current_signature):
        return None
    outputs = (
        str(view.get("live_feed_html", "")),
        str(view.get("emerging_signals_html", "")),
        str(view.get("interpretation_markdown", "")),
        str(view.get("historical_learning_markdown", "")),
    )
    return outputs if all(part.strip() for part in outputs) else None


def save_rendered_outputs(cache_key: str, signature: list[dict[str, Any]], outputs: tuple[str, str, str, str], path: str | Path | None = None) -> dict[str, Any]:
    cache = load_render_cache(path)
    view = {
        "last_signal_signature": signature,
        "live_feed_html": outputs[0],
        "emerging_signals_html": outputs[1],
        "interpretation_markdown": outputs[2],
        "historical_learning_markdown": outputs[3],
        "last_rendered_at": datetime.now(UTC).isoformat(),
    }
    cache.update(view)
    cache.setdefault("views", {})[cache_key] = view
    return write_json(render_cache_path(path), cache)


def clear_render_cache(path: str | Path | None = None) -> None:
    target = render_cache_path(path)
    if target.exists():
        target.unlink()


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
        if abs(_adaptive_score(signal) - _adaptive_score(old)) > _ADAPTIVE_DELTA_THRESHOLD:
            return True
    return False


def rank_signals_for_display(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank by collective intelligence so stronger emerging issues rise smoothly."""
    return sorted(signals or [], key=_ranking_score, reverse=True)


def signal_signature(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return compact fields used for render-cache comparison, excluding timestamps."""
    return [
        {
            "key": _signal_key(signal),
            "urgency": str(signal.get("urgency", "")),
            "momentum": str(signal.get("momentum", "")),
            "forecast_direction": str(signal.get("forecast_direction") or signal.get("predicted_direction") or ""),
            "confidence_score": round(_number(signal.get("confidence_score")), 2),
            "adaptive_intelligence_score": round(_adaptive_score(signal), 2),
            "ranking_score": round(_ranking_score(signal), 2),
        }
        for signal in _normalize(signals)
    ]


def _normalize(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(signal) for signal in signals if isinstance(signal, dict)]


def _signal_key(signal: dict[str, Any]) -> str:
    key = signal.get("key") or signal.get("semantic_cluster") or signal.get("signal_cluster") or signal.get("signal_topic") or signal.get("topic") or ""
    return " ".join(str(key).lower().strip().split())


def _changed_label(previous: dict[str, Any], current: dict[str, Any], field: str) -> bool:
    return str(previous.get(field, "")).lower() != str(current.get(field, "")).lower()


def _adaptive_score(signal: dict[str, Any]) -> float:
    return _number(signal.get("adaptive_intelligence_score"), _number(signal.get("behavioral_intelligence_score"), _number(signal.get("priority_score"), 50)))


def _ranking_score(signal: dict[str, Any]) -> float:
    urgency = {"high": 100.0, "medium": 62.0, "low": 35.0}.get(str(signal.get("urgency", "")).lower(), _number(signal.get("urgency_score"), 50))
    momentum = {"breakout": 100.0, "rising": 82.0, "stable": 55.0, "declining": 28.0}.get(str(signal.get("momentum", "")).lower(), 50.0)
    forecast = 78.0 if str(signal.get("forecast_direction") or signal.get("predicted_direction", "")).lower() == "rising" else 50.0
    outcome = _number(signal.get("historical_accuracy_score"), 50)
    return (
        _adaptive_score(signal) * 0.20
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