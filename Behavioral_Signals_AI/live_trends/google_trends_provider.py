"""Google Trends compatible aggregate trend provider."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .trend_classifier import classify_trend_batch
from .trend_normalizer import assert_aggregate_privacy, normalize_trend_records
from .trend_provider_base import TrendProviderResult, TrendProviderStatus

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"
APIFY_ENDPOINT_ENV = "APIFY_TRENDS_ENDPOINT"


class GoogleTrendsProvider:
    provider_name = "google"

    def __init__(self, api_key: str | None = None, serpapi_key: str | None = None, apify_token: str | None = None) -> None:
        self.api_key = (api_key if api_key is not None else os.getenv("GOOGLE_TRENDS_API_KEY", "")).strip()
        self.serpapi_key = (serpapi_key if serpapi_key is not None else os.getenv("SERPAPI_API_KEY", "")).strip()
        self.apify_token = (apify_token if apify_token is not None else os.getenv("APIFY_API_TOKEN", "")).strip()
        self.apify_endpoint = os.getenv(APIFY_ENDPOINT_ENV, "").strip()

    def is_available(self) -> bool:
        return bool(self.api_key or self.serpapi_key or (self.apify_token and self.apify_endpoint))

    def fetch_trends(self, location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
        if not self.is_available():
            raise RuntimeError("Google Trends compatible provider credentials are not configured.")
        try:
            if self.serpapi_key or self.api_key:
                records = self._fetch_serpapi_trending_now(location=location, limit=int(limit))
                source = "Google Trends"
            else:
                records = self._fetch_apify_endpoint(location=location, limit=int(limit))
                source = "Apify"
            status = TrendProviderStatus(self.provider_name, True, "google", f"{source} aggregate trends loaded from live provider.")
            return TrendProviderResult(records=records, provider=self.provider_name, source_label=source, is_live=True, status=status)
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            status = TrendProviderStatus(self.provider_name, False, "google", f"Google-compatible trend provider unavailable: {exc}")
            return TrendProviderResult(records=[], provider=self.provider_name, source_label="Google Trends", is_live=False, status=status, warnings=[str(exc)])

    def _fetch_serpapi_trending_now(self, location: str, limit: int) -> list[dict[str, Any]]:
        geo = "KE" if location in {"Kenya", "Nairobi"} else "US"
        params = {
            "engine": "google_trends_trending_now",
            "geo": geo,
            "api_key": self.serpapi_key or self.api_key,
        }
        request = Request(f"{SERPAPI_ENDPOINT}?{urlencode(params)}")
        request.add_header("User-Agent", "SignalAI/1.0")
        with urlopen(request, timeout=20) as response:  # noqa: S310 - fixed public API endpoint
            payload = json.loads(response.read().decode("utf-8"))
        items = _extract_google_items(payload)
        raw_records = []
        for index, item in enumerate(items[: max(1, int(limit))], start=1):
            raw_records.append(
                {
                    "trend_name": item.get("query") or item.get("title") or item.get("name") or f"Trend {index}",
                    "rank": index,
                    "volume": item.get("search_volume") or item.get("traffic") or item.get("volume"),
                    "growth_indicator": item.get("growth") or item.get("increase_percentage"),
                    "location": location,
                    "source": "Google Trends",
                    "is_live": True,
                }
            )
        normalized = normalize_trend_records(raw_records, platform="Google Trends", location=location)
        return classify_trend_batch(assert_aggregate_privacy(normalized))

    def _fetch_apify_endpoint(self, location: str, limit: int) -> list[dict[str, Any]]:
        separator = "&" if "?" in self.apify_endpoint else "?"
        request = Request(f"{self.apify_endpoint}{separator}{urlencode({'location': location, 'limit': int(limit)})}")
        request.add_header("Authorization", f"Bearer {self.apify_token}")
        request.add_header("User-Agent", "SignalAI/1.0")
        with urlopen(request, timeout=20) as response:  # noqa: S310 - user-configured provider endpoint
            payload = json.loads(response.read().decode("utf-8"))
        items = payload if isinstance(payload, list) else payload.get("items", []) or payload.get("trends", [])
        normalized = normalize_trend_records(items[: max(1, int(limit))], platform="Apify", location=location)
        return classify_trend_batch(assert_aggregate_privacy(normalized))


def _extract_google_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("trending_searches", "daily_searches", "trends", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []