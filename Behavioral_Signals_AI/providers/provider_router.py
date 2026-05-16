"""Multi-provider aggregate public signal routing for Behavioral Signals AI."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.providers.provider_base import ProviderStatus, assert_privacy_safe_signals, normalize_signals
from Behavioral_Signals_AI.providers.provider_registry import build_provider_registry, phase_one_provider_keys

VALID_MODES = {"auto", "demo", "google", "serpapi", "pytrends", "x", "gdelt", "news"}


@dataclass
class AggregateSignalRouteResult:
    signals: list[dict[str, Any]]
    source_label: str
    is_live: bool
    mode_badge: str
    provider_statuses: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def fetch_aggregate_signals(location: str = "Kenya", limit: int = 10) -> AggregateSignalRouteResult:
    """Route across configured providers, merge outputs, dedupe, and fallback safely."""

    mode = _requested_mode()
    if mode == "demo":
        return _demo_result(location, limit, warnings=[])

    registry = build_provider_registry()
    keys = _provider_keys_for_mode(mode)
    all_signals: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    warnings: list[str] = []

    for key in keys:
        provider = registry.get(key)
        if provider is None:
            continue
        available = bool(provider.is_available())
        statuses.append({"provider": key, "provider_type": getattr(provider, "provider_type", "unknown"), "available": available})
        if not available:
            continue
        result = provider.fetch_signals(location=location, limit=limit)
        statuses.append({"provider": result.provider, "provider_type": result.provider_type, "available": bool(result.signals), "message": result.status.message})
        warnings.extend(result.warnings)
        all_signals.extend(result.signals)
        if len(all_signals) >= limit and mode != "auto":
            break

    ranked = rank_and_deduplicate_signals(all_signals)[: max(1, int(limit))]
    if not ranked:
        return _demo_result(location, limit, warnings=warnings)

    safe = assert_privacy_safe_signals(ranked)
    source_label = _source_label(safe)
    return AggregateSignalRouteResult(
        signals=safe,
        source_label=source_label,
        is_live=True,
        mode_badge="Live Kenya signals",
        provider_statuses=statuses,
        warnings=warnings[:3],
    )


def rank_and_deduplicate_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for signal in signals:
        key = _topic_key(str(signal.get("signal_name", "")))
        score = _signal_score(signal)
        current = deduped.get(key)
        if current is None or score > _signal_score(current):
            deduped[key] = signal
    return sorted(deduped.values(), key=_signal_score, reverse=True)


def _requested_mode() -> str:
    mode = os.getenv("SIGNAL_TRENDS_MODE", "auto").strip().lower() or "auto"
    return mode if mode in VALID_MODES else "auto"


def _provider_keys_for_mode(mode: str) -> list[str]:
    if mode == "auto":
        return phase_one_provider_keys()
    if mode == "google":
        return ["google", "serpapi", "pytrends"]
    return [mode]


def _demo_result(location: str, limit: int, warnings: list[str]) -> AggregateSignalRouteResult:
    raw = [
        {"signal_name": "maize flour prices", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "food_agriculture", "location": location, "volume": 185000, "growth": "rising"},
        {"signal_name": "jobs in Nairobi", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "jobs", "location": location, "volume": 140000, "growth": "rising"},
        {"signal_name": "cheap smartphones", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "technology", "location": location, "volume": 112000, "growth": "rising"},
        {"signal_name": "hospital near me", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "health", "location": location, "volume": 98000, "growth": "steady"},
        {"signal_name": "fuel prices", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "prices", "location": location, "volume": 176000, "growth": "rising"},
        {"signal_name": "digital lending", "source": "Fallback aggregate intelligence", "provider_type": "demo", "category": "finance", "location": location, "volume": 76000, "growth": "steady"},
    ][: max(1, int(limit))]
    signals = normalize_signals(raw, source="Fallback aggregate intelligence", provider_type="demo", location=location)
    return AggregateSignalRouteResult(
        signals=assert_privacy_safe_signals(signals),
        source_label="Fallback aggregate intelligence",
        is_live=False,
        mode_badge="Fallback aggregate intelligence",
        provider_statuses=[{"provider": "demo", "provider_type": "demo", "available": True}],
        warnings=warnings[:3],
    )


def _source_label(signals: list[dict[str, Any]]) -> str:
    sources = sorted({str(signal.get("source", "Aggregate signals")) for signal in signals})
    return ", ".join(sources[:3]) + (" + more" if len(sources) > 3 else "")


def _signal_score(signal: dict[str, Any]) -> float:
    relevance = float(signal.get("demand_relevance") or 0.0)
    confidence = float(signal.get("confidence") or 0.0)
    volume = float(signal.get("volume") or 0.0)
    return (relevance * 55) + (confidence * 35) + min(volume / 100000.0, 10)


def _topic_key(name: str) -> str:
    lowered = name.lower().replace("#", "")
    tokens = [token for token in lowered.replace("-", " ").split() if token not in {"the", "a", "and", "in", "near", "me"}]
    return " ".join(tokens[:4]) or lowered or datetime.now(UTC).isoformat()