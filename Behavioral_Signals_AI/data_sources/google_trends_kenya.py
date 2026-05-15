"""Kenya search trend connector using optional SerpAPI credentials."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    api_key = os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return []
    params = urlencode({"engine": "google_trends_trending_now", "geo": "KE", "api_key": api_key})
    url = f"https://serpapi.com/search.json?{params}"
    try:
        with urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return []
    trends = payload.get("trending_searches") or payload.get("trends") or []
    now = datetime.now(UTC).isoformat()
    records = []
    for item in trends[:limit]:
        if isinstance(item, str):
            title = item
            volume = 60
        else:
            title = item.get("query") or item.get("title") or item.get("name") or "Kenya search trend"
            volume = item.get("search_volume") or item.get("traffic") or item.get("volume") or 65
        records.append({
            "topic": str(title),
            "source_type": "search_trend",
            "location": location,
            "relative_interest": volume,
            "engagement_signal": 55,
            "growth_signal": 72,
            "sentiment_signal": 0,
            "timestamp": now,
            "source_summary": "Search trends",
            "privacy_level": "aggregate_public",
        })
    return records