"""Cache helpers for resilient Kenya live signal rendering."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.data_sources import fallback_sample_source
from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

DEFAULT_CACHE_PATH = Path(os.getenv("SIGNAL_LIVE_SIGNAL_CACHE", "Behavioral_Signals_AI/outputs/latest_live_signals.json"))


def cache_path(path: str | Path | None = None) -> Path:
    return Path(path or os.getenv("SIGNAL_LIVE_SIGNAL_CACHE", str(DEFAULT_CACHE_PATH)))


def initialize_signal_cache(path: str | Path | None = None) -> dict[str, Any]:
    target = cache_path(path)
    if target.exists():
        data = read_signal_cache(target)
        if data.get("signals"):
            return data
    signals = _fallback_fused_signals()
    payload = _payload(signals, status="initialized_from_sample")
    write_signal_cache(payload, target)
    return payload


def refresh_signal_cache(location: str = "Kenya", path: str | Path | None = None) -> dict[str, Any]:
    target = cache_path(path)
    try:
        signals = fuse_kenya_signals(location, "All", "All")
        if not signals:
            raise RuntimeError("Kenya signal fusion returned no signals")
        payload = _payload(signals, status="live_or_near_live")
        write_signal_cache(payload, target)
        return payload
    except Exception as exc:
        cached = read_signal_cache(target)
        if cached.get("signals"):
            cached["status"] = "using_cached_last_success"
            cached["warning"] = str(exc)
            return cached
        signals = _fallback_fused_signals()
        payload = _payload(signals, status="sample_aggregate_signal", warning=str(exc))
        write_signal_cache(payload, target)
        return payload


def read_signal_cache(path: str | Path | None = None) -> dict[str, Any]:
    data = read_json(cache_path(path), {"signals": [], "last_updated": "", "status": "missing"})
    if isinstance(data, dict):
        data.setdefault("signals", [])
        data.setdefault("last_updated", datetime.now(UTC).isoformat())
        return data
    return {"signals": [], "last_updated": "", "status": "missing"}


def get_cached_or_fallback_signals(path: str | Path | None = None) -> dict[str, Any]:
    cached = read_signal_cache(path)
    if cached.get("signals"):
        return cached
    return initialize_signal_cache(path)


def write_signal_cache(payload: dict[str, Any], path: str | Path | None = None) -> None:
    write_json(cache_path(path), payload)


def _payload(signals: list[dict[str, Any]], status: str, warning: str | None = None) -> dict[str, Any]:
    payload = {
        "last_updated": datetime.now(UTC).isoformat(),
        "status": status,
        "signals": signals,
        "privacy_level": "aggregate_public",
    }
    if warning:
        payload["warning"] = warning
    return payload


def _fallback_fused_signals() -> list[dict[str, Any]]:
    from Behavioral_Signals_AI.signal_engine.kenya_interpretation_engine import interpret_kenya_signal

    signals: list[dict[str, Any]] = []
    for index, record in enumerate(fallback_sample_source.collect("Kenya", limit=8)):
        priority = max(45.0, min(95.0, float(record.get("relative_interest", 55)) * 0.5 + float(record.get("growth_signal", 55)) * 0.5))
        signal = {
            "signal_topic": str(record.get("topic", "Kenya aggregate signal")),
            "signal_category": str(record.get("category", "other")),
            "demand_level": "High" if priority >= 74 else "Moderate" if priority >= 50 else "Low",
            "opportunity_level": "High" if priority >= 76 else "Moderate" if priority >= 50 else "Low",
            "unmet_demand_likelihood": "High" if priority >= 78 else "Medium" if priority >= 50 else "Low",
            "urgency": "High" if priority >= 80 else "Medium" if priority >= 52 else "Low",
            "geographic_scope": "Kenya-wide",
            "source_summary": str(record.get("source_summary", "Sample aggregate signal")),
            "confidence_score": round(min(92.0, 52.0 + priority * 0.35), 1),
            "last_updated": str(record.get("timestamp")),
            "priority_score": round(priority - index, 2),
            "momentum": "Rising" if priority >= 65 else "Stable",
            "privacy_level": "aggregate_public",
        }
        interpretation = interpret_kenya_signal(signal)
        signal.update(interpretation)
        signal["recommended_action"] = interpretation["near_term_monitoring_recommendation"]
        signals.append(signal)
    signals.sort(key=lambda item: float(item.get("priority_score", 0)), reverse=True)
    return signals
