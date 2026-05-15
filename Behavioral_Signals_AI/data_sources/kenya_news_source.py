"""Kenya public news connector using optional News API credentials."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

KEYWORDS = ["Kenya prices", "Kenya jobs", "Kenya food", "Kenya health", "Kenya fuel", "Kenya water"]


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return []
    params = urlencode({"q": " OR ".join(KEYWORDS), "language": "en", "pageSize": min(limit, 20), "sortBy": "publishedAt"})
    request = Request(f"https://newsapi.org/v2/everything?{params}", headers={"X-Api-Key": api_key})
    try:
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return []
    now = datetime.now(UTC).isoformat()
    records = []
    for article in payload.get("articles", [])[:limit]:
        title = article.get("title") or "Kenya public news signal"
        records.append({
            "topic": title,
            "source_type": "news_public",
            "location": location,
            "relative_interest": 68,
            "engagement_signal": 58,
            "growth_signal": 62,
            "sentiment_signal": -0.05,
            "timestamp": article.get("publishedAt") or now,
            "source_summary": "Public news",
            "privacy_level": "aggregate_public",
        })
    return records