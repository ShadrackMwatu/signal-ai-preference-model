"""Demo aggregate trend provider used when live credentials are unavailable."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .trend_classifier import classify_trend_batch
from .trend_normalizer import assert_aggregate_privacy, normalize_trend_records
from .trend_provider_base import TrendProviderResult, TrendProviderStatus


class FallbackDemoTrendProvider:
    provider_name = "demo"

    def is_available(self) -> bool:
        return True

    def fetch_trends(self, location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
        records = get_demo_trends(location=location, limit=limit)
        status = TrendProviderStatus(
            provider=self.provider_name,
            available=True,
            mode="demo",
            message="Demo aggregate trend feed is active because no live provider was selected or available.",
        )
        return TrendProviderResult(records=records, provider=self.provider_name, source_label="Demo fallback", is_live=False, status=status)


def get_demo_trends(location: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    fetched_at = datetime.now(UTC).isoformat()
    catalog: dict[str, list[tuple[str, int, int]]] = {
        "Kenya": [
            ("Cost of living", 1, 185000),
            ("Fuel prices", 2, 132000),
            ("Jobs and youth employment", 3, 118000),
            ("Maize prices", 4, 96000),
            ("Healthcare access", 5, 86000),
            ("Digital lending", 6, 76000),
            ("County water supply", 7, 64000),
            ("SME credit", 8, 53000),
        ],
        "Nairobi": [
            ("Nairobi transport", 1, 142000),
            ("Housing delivery", 2, 81000),
            ("Last mile delivery", 3, 69000),
            ("Coffee shops", 4, 51000),
            ("Ride hailing", 5, 46000),
            ("School transport", 6, 41000),
        ],
        "Global": [
            ("AI workflows", 1, 420000),
            ("Climate insurance", 2, 330000),
            ("Digital payments", 3, 305000),
            ("Telehealth growth", 4, 271000),
            ("Food security", 5, 208000),
        ],
    }
    raw_records: list[dict[str, Any]] = []
    for trend_name, rank, volume in catalog.get(location, catalog["Kenya"])[: max(1, int(limit))]:
        raw_records.append(
            {
                "trend_name": trend_name,
                "rank": rank,
                "volume": volume,
                "location": location,
                "timestamp": fetched_at,
                "source": "Demo fallback",
                "is_live": False,
            }
        )
    normalized = normalize_trend_records(raw_records, platform="Demo fallback", location=location)
    return classify_trend_batch(assert_aggregate_privacy(normalized))