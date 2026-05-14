"""Route live trend requests across configured aggregate providers."""

from __future__ import annotations

import os
from typing import Any

from .fallback_demo_provider import FallbackDemoTrendProvider, get_demo_trends
from .google_trends_provider import GoogleTrendsProvider
from .trend_provider_base import TrendProviderResult, TrendProviderStatus
from .x_trends_provider import XTrendsProvider

VALID_MODES = {"auto", "demo", "x", "google", "serpapi", "apify"}


def get_trend_provider_status() -> dict[str, Any]:
    mode = _requested_mode()
    return {
        "mode": mode,
        "x_available": XTrendsProvider().is_available(),
        "google_available": GoogleTrendsProvider().is_available(),
        "demo_available": True,
        "privacy": "aggregate_trends_only",
    }


def fetch_live_trends(location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
    """Return standardized public aggregate trends using configured provider priority."""

    mode = _requested_mode()
    providers = _providers_for_mode(mode)
    warnings: list[str] = []
    for provider in providers:
        if not provider.is_available():
            warnings.append(f"{provider.provider_name} credentials unavailable")
            continue
        result = provider.fetch_trends(location=location, limit=limit)
        if result.records:
            result.warnings = warnings + result.warnings
            return result
        warnings.extend(result.warnings or [result.status.message])

    fallback = FallbackDemoTrendProvider().fetch_trends(location=location, limit=limit)
    fallback.warnings = warnings + ["Live trend credentials unavailable or provider returned no records; demo fallback used."]
    fallback.status = TrendProviderStatus("demo", True, mode, "Demo fallback used after live provider routing.")
    return fallback


def _requested_mode() -> str:
    mode = os.getenv("SIGNAL_TRENDS_MODE", "auto").strip().lower() or "auto"
    return mode if mode in VALID_MODES else "auto"


def _providers_for_mode(mode: str):
    if mode == "demo":
        return [FallbackDemoTrendProvider()]
    if mode == "x":
        return [XTrendsProvider()]
    if mode in {"google", "serpapi", "apify"}:
        return [GoogleTrendsProvider()]
    return [XTrendsProvider(), GoogleTrendsProvider()]


__all__ = ["fetch_live_trends", "get_demo_trends", "get_trend_provider_status"]