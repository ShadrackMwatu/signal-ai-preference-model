"""SerpAPI Google Trends compatible aggregate search provider."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"


class SerpApiSearchProvider:
    provider_name = "serpapi"
    provider_type = "search"
    source_label = "SerpAPI Google Trends"

    def is_available(self) -> bool:
        return bool(os.getenv("SERPAPI_API_KEY", "").strip() or os.getenv("GOOGLE_TRENDS_API_KEY", "").strip())

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        key = os.getenv("SERPAPI_API_KEY", "").strip() or os.getenv("GOOGLE_TRENDS_API_KEY", "").strip()
        if not key:
            status = ProviderStatus(self.provider_name, self.provider_type, False, False, "serpapi", "SerpAPI key unavailable.")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])
        try:
            params = {"engine": "google_trends_trending_now", "geo": "KE", "api_key": key}
            request = Request(f"{SERPAPI_ENDPOINT}?{urlencode(params)}")
            request.add_header("User-Agent", "SignalAI/1.0")
            with urlopen(request, timeout=12) as response:  # noqa: S310 - fixed public API endpoint
                payload = json.loads(response.read().decode("utf-8"))
            items = _extract_items(payload)[: max(1, int(limit))]
            raw = [
                {
                    "signal_name": item.get("query") or item.get("title") or item.get("name") or f"Search trend {idx}",
                    "source": self.source_label,
                    "volume": item.get("search_volume") or item.get("traffic"),
                    "growth": item.get("growth") or item.get("increase_percentage"),
                    "location": location,
                }
                for idx, item in enumerate(items, start=1)
            ]
            status = ProviderStatus(self.provider_name, self.provider_type, True, True, "serpapi", "Search trend signals loaded.")
            return ProviderResult(normalize_signals(raw, source=self.source_label, provider_type=self.provider_type, location=location), self.provider_name, self.provider_type, self.source_label, True, status)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            status = ProviderStatus(self.provider_name, self.provider_type, False, True, "serpapi", f"Search provider unavailable: {exc}")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])


def _extract_items(payload: dict) -> list[dict]:
    for key in ("trending_searches", "daily_searches", "trends", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []