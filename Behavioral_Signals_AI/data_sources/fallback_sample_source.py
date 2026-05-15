"""Kenya sample aggregate signals used when live public sources are unavailable."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def collect(location: str = "Kenya", limit: int = 12) -> list[dict[str, Any]]:
    now = datetime.now(UTC).isoformat()
    records = [
        ("maize flour prices", "food and agriculture", "search_trend", 93, 68, 82, -0.32, "Search trends + public news + food price data"),
        ("fuel prices Kenya", "energy", "news_public", 89, 72, 78, -0.28, "Public news + macro indicators"),
        ("jobs in Nairobi", "jobs and labour market", "search_trend", 86, 70, 71, 0.05, "Search trends + public discussion"),
        ("cheap smartphones Kenya", "technology and digital economy", "search_trend", 84, 63, 69, 0.18, "Search trends + digital demand signals"),
        ("hospital near me", "health", "search_trend", 80, 55, 64, -0.12, "Search trends + public service concern"),
        ("water shortage Makueni", "water and sanitation", "news_public", 77, 58, 75, -0.35, "Public news + climate signals"),
        ("fertilizer prices Nakuru", "food and agriculture", "search_trend", 74, 52, 68, -0.18, "Agriculture signals + search trends"),
        ("rent in Nairobi", "housing", "search_trend", 72, 54, 61, -0.08, "Search trends + affordability signals"),
        ("school fees Kenya", "education", "search_trend", 70, 48, 58, -0.04, "Search trends + household pressure"),
        ("digital loans Kenya", "finance and credit", "search_trend", 68, 62, 60, -0.02, "Search trends + finance signals"),
    ]
    output = []
    for topic, category, source_type, interest, engagement, growth, sentiment, source_summary in records[:limit]:
        output.append(
            {
                "topic": topic,
                "category": category,
                "source_type": source_type,
                "location": location,
                "relative_interest": interest,
                "engagement_signal": engagement,
                "growth_signal": growth,
                "sentiment_signal": sentiment,
                "timestamp": now,
                "source_summary": source_summary,
                "sample_signal": True,
                "privacy_level": "aggregate_public",
            }
        )
    return output