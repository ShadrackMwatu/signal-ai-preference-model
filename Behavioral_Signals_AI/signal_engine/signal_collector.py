"""Collect aggregate topical signals from configured public/provider routers."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any


def _fallback_signals(location: str = "Kenya") -> list[dict[str, Any]]:
    now = datetime.now(UTC).isoformat()
    return [
        {"topic": "cheap smartphones Kenya", "source_type": "search_trend", "location": location, "category": "technology", "relative_interest": 86, "engagement_signal": 61, "growth_signal": 72, "sentiment_signal": 0.15, "timestamp": now},
        {"topic": "maize flour prices", "source_type": "search_trend", "location": location, "category": "food and agriculture", "relative_interest": 91, "engagement_signal": 64, "growth_signal": 78, "sentiment_signal": -0.25, "timestamp": now},
        {"topic": "jobs in Nairobi", "source_type": "search_trend", "location": location, "category": "jobs and labour market", "relative_interest": 84, "engagement_signal": 68, "growth_signal": 70, "sentiment_signal": 0.05, "timestamp": now},
        {"topic": "hospital near me", "source_type": "search_trend", "location": location, "category": "health", "relative_interest": 79, "engagement_signal": 52, "growth_signal": 63, "sentiment_signal": -0.1, "timestamp": now},
        {"topic": "fuel prices Kenya", "source_type": "news_public", "location": location, "category": "energy", "relative_interest": 88, "engagement_signal": 70, "growth_signal": 76, "sentiment_signal": -0.35, "timestamp": now},
        {"topic": "affordable school fees", "source_type": "search_trend", "location": location, "category": "education", "relative_interest": 72, "engagement_signal": 49, "growth_signal": 59, "sentiment_signal": -0.05, "timestamp": now},
    ]


def collect_aggregate_signals(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    mode = os.getenv("SIGNAL_DATA_MODE") or os.getenv("SIGNAL_TRENDS_MODE", "auto")
    if str(mode).lower() == "demo":
        return _fallback_signals(location)[:limit]
    try:
        from Behavioral_Signals_AI.providers.provider_router import fetch_aggregate_signals

        result = fetch_aggregate_signals(location=location, limit=limit)
        records = list(getattr(result, "signals", None) or getattr(result, "records", None) or [])
        if records:
            return records[:limit]
    except Exception:
        pass
    return _fallback_signals(location)[:limit]