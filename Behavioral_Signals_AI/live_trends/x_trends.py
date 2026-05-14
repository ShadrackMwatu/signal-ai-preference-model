"""Compatibility helpers for X/Twitter aggregate trend fetching."""

from __future__ import annotations

from typing import Any

from .fallback_demo_provider import get_demo_trends
from .trend_router import fetch_live_trends
from .x_trends_provider import X_TRENDS_ENDPOINT, XTrendsProvider, load_location_config


def fetch_x_trends(location: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    """Fetch X trends when configured, otherwise return safe demo aggregate trends."""

    result = fetch_live_trends(location=location, limit=limit)
    return result.records


__all__ = ["XTrendsProvider", "X_TRENDS_ENDPOINT", "fetch_x_trends", "get_demo_trends", "load_location_config"]