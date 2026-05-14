"""Route dashboard trend requests through the multi-source aggregate signal provider layer."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.live_trends.fallback_demo_provider import get_demo_trends
from Behavioral_Signals_AI.live_trends.trend_provider_base import TrendProviderResult, TrendProviderStatus
from Behavioral_Signals_AI.providers.provider_router import fetch_aggregate_signals
from Behavioral_Signals_AI.providers.provider_registry import build_provider_registry


def get_trend_provider_status() -> dict[str, Any]:
    registry = build_provider_registry()
    providers = {
        key: {
            "provider_type": getattr(provider, "provider_type", "unknown"),
            "available": bool(provider.is_available()),
        }
        for key, provider in registry.items()
    }
    return {
        "providers": providers,
        "x_available": bool(providers.get("x", {}).get("available", False)),
        "google_available": bool(
            providers.get("google", {}).get("available", False)
            or providers.get("serpapi", {}).get("available", False)
            or providers.get("pytrends", {}).get("available", False)
        ),
        "demo_available": True,
        "privacy": "aggregate_public_signals_only",
    }


def fetch_live_trends(location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
    """Return dashboard-compatible trend records from the multi-source provider router."""

    routed = fetch_aggregate_signals(location=location, limit=limit)
    records = [_signal_to_trend_record(signal, routed.mode_badge) for signal in routed.signals]
    status = TrendProviderStatus(
        provider="multi_source_router",
        available=bool(records),
        mode="live" if routed.is_live else "demo",
        message=routed.mode_badge,
    )
    return TrendProviderResult(
        records=records,
        provider="multi_source_router",
        source_label=routed.source_label,
        is_live=routed.is_live,
        status=status,
        warnings=routed.warnings,
    )


def _signal_to_trend_record(signal: dict[str, Any], mode_badge: str) -> dict[str, Any]:
    source = str(signal.get("source") or "Aggregate signals")
    return {
        "trend_name": signal.get("signal_name", "Aggregate signal"),
        "platform": source,
        "source": source,
        "provider_type": signal.get("provider_type"),
        "location": signal.get("location", "Kenya"),
        "rank": 1,
        "volume": signal.get("volume"),
        "tweet_volume": signal.get("volume") if signal.get("provider_type") == "social" else None,
        "growth_indicator": signal.get("growth") or "not available",
        "category": signal.get("category", "general_public_interest"),
        "timestamp": signal.get("timestamp"),
        "fetched_at": signal.get("timestamp"),
        "confidence": signal.get("confidence"),
        "relevance_to_demand": signal.get("demand_relevance"),
        "privacy_level": signal.get("privacy_level", "aggregate_public"),
        "possible_policy_or_business_implication": _implication(signal),
        "mode_badge": mode_badge,
    }


def _implication(signal: dict[str, Any]) -> str:
    name = str(signal.get("signal_name", "This signal"))
    category = str(signal.get("category", "general_public_interest")).replace("_", " ")
    provider_type = str(signal.get("provider_type", "aggregate"))
    return f"{name} is a {provider_type} signal linked to {category}; monitor for revealed demand, pressure, unmet need, or market opportunity."


__all__ = ["fetch_live_trends", "get_demo_trends", "get_trend_provider_status"]