"""Schemas for aggregated place activity indicators only."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from typing import Literal

PopularityLevel = Literal["low", "moderate", "high", "very_high"]
ActivityIndicator = Literal["increasing", "stable", "decreasing"]
ActivityTrend = Literal["rising", "stable", "falling"]


@dataclass(slots=True)
class AggregatedPlaceActivityIndicator:
    region: str
    county: str
    place_name: str
    place_id: str
    place_category: str
    demand_category: str
    rating: float
    review_count: int
    opening_hours_status: str
    business_status: str
    place_prominence: float
    popularity_level: PopularityLevel
    activity_indicator: ActivityIndicator
    estimated_activity_trend: ActivityTrend
    source: str
    confidence: float
    privacy_status: str = "approved"
    date: str = ""

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["date"] = payload["date"] or today_iso()
        return payload


def today_iso() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(UTC).isoformat()