"""News API provider for aggregate public information signals."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsApiProvider:
    provider_name = "newsapi"
    provider_type = "news"
    source_label = "News API"

    def is_available(self) -> bool:
        return bool(os.getenv("NEWS_API_KEY", "").strip())

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        key = os.getenv("NEWS_API_KEY", "").strip()
        if not key:
            status = ProviderStatus(self.provider_name, self.provider_type, False, False, "news", "NEWS_API_KEY unavailable.")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])
        try:
            params = {"q": "Kenya economy OR prices OR jobs OR food OR health", "language": "en", "pageSize": max(1, int(limit)), "apiKey": key}
            request = Request(f"{NEWSAPI_ENDPOINT}?{urlencode(params)}")
            request.add_header("User-Agent", "SignalAI/1.0")
            with urlopen(request, timeout=10) as response:  # noqa: S310 - fixed public API endpoint
                payload = json.loads(response.read().decode("utf-8"))
            raw = [{"signal_name": item.get("title", "Kenya public information signal"), "source": self.source_label, "location": location, "growth": "news context"} for item in payload.get("articles", [])[: max(1, int(limit))]]
            status = ProviderStatus(self.provider_name, self.provider_type, True, True, "news", "News API context loaded.")
            return ProviderResult(normalize_signals(raw, source=self.source_label, provider_type=self.provider_type, location=location), self.provider_name, self.provider_type, self.source_label, True, status)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            status = ProviderStatus(self.provider_name, self.provider_type, False, True, "news", f"News API unavailable: {exc}")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])