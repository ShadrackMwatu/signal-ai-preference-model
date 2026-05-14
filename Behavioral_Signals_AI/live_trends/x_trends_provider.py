"""X/Twitter public aggregate trend provider."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .trend_classifier import classify_trend_batch
from .trend_normalizer import assert_aggregate_privacy, normalize_trend_records
from .trend_provider_base import TrendProviderResult, TrendProviderStatus

X_TRENDS_ENDPOINT = "https://api.twitter.com/1.1/trends/place.json"
DEFAULT_LOCATIONS = {
    "Kenya": {"woeid": 23424863},
    "Nairobi": {"woeid": 1528488},
    "Global": {"woeid": 1},
}


class XTrendsProvider:
    provider_name = "x"

    def __init__(self, bearer_token: str | None = None, locations_path: str | Path | None = None) -> None:
        self.bearer_token = (bearer_token if bearer_token is not None else os.getenv("X_BEARER_TOKEN", "")).strip()
        self.locations_path = Path(locations_path) if locations_path else Path(__file__).resolve().parent / "config" / "locations.json"

    def is_available(self) -> bool:
        return bool(self.bearer_token)

    def fetch_trends(self, location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
        if not self.is_available():
            raise RuntimeError("X_BEARER_TOKEN is not configured.")
        locations = load_location_config(self.locations_path)
        if location not in locations:
            raise ValueError(f"Unsupported X trend location: {location}")
        try:
            records = self._fetch_live_trends(location, int(locations[location]["woeid"]), int(limit))
            status = TrendProviderStatus(self.provider_name, True, "x", "X aggregate trends loaded from live API.")
            return TrendProviderResult(records=records, provider=self.provider_name, source_label="X", is_live=True, status=status)
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            status = TrendProviderStatus(self.provider_name, False, "x", f"X trend API unavailable: {exc}")
            return TrendProviderResult(records=[], provider=self.provider_name, source_label="X", is_live=False, status=status, warnings=[str(exc)])

    def _fetch_live_trends(self, location: str, woeid: int, limit: int) -> list[dict[str, Any]]:
        query = urlencode({"id": int(woeid)})
        request = Request(f"{X_TRENDS_ENDPOINT}?{query}")
        request.add_header("Authorization", f"Bearer {self.bearer_token}")
        request.add_header("User-Agent", "SignalAI/1.0")
        with urlopen(request, timeout=20) as response:  # noqa: S310 - fixed public API endpoint
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, list) or not payload:
            raise ValueError("Unexpected X trends payload structure")
        trend_items = payload[0].get("trends", [])
        raw_records = []
        for index, trend in enumerate(trend_items[: max(1, int(limit))], start=1):
            raw_records.append(
                {
                    "trend_name": trend.get("name", f"Trend {index}"),
                    "rank": index,
                    "volume": trend.get("tweet_volume"),
                    "tweet_volume": trend.get("tweet_volume"),
                    "location": location,
                    "source": "X",
                    "is_live": True,
                }
            )
        normalized = normalize_trend_records(raw_records, platform="X", location=location)
        return classify_trend_batch(assert_aggregate_privacy(normalized))


def load_location_config(path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    if path and Path(path).exists():
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload:
                return payload
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULT_LOCATIONS


def fetch_x_trends(location: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    """Compatibility helper returning records or an empty list if unavailable."""

    result = XTrendsProvider().fetch_trends(location=location, limit=limit)
    return result.records