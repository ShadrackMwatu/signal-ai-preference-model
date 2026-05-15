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
    popularity_level: PopularityLevel
    activity_indicator: ActivityIndicator
    review_activity_level: PopularityLevel
    estimated_activity_trend: ActivityTrend
    place_prominence: float
    date: str
    source: str
    confidence: float
    privacy_status: str = "approved"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def today_iso() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(UTC).isoformat()