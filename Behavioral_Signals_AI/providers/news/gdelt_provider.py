"""GDELT public news context provider for aggregate economic pressure signals."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


class GdeltNewsProvider:
    provider_name = "gdelt"
    provider_type = "news"
    source_label = "GDELT"

    def is_available(self) -> bool:
        return os.getenv("SIGNAL_ENABLE_GDELT", "").strip().lower() in {"1", "true", "yes"}

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        if not self.is_available():
            status = ProviderStatus(self.provider_name, self.provider_type, False, False, "gdelt", "GDELT disabled by default; set SIGNAL_ENABLE_GDELT=1 to enable public news context.")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])
        try:
            params = {"query": "Kenya economy OR prices OR jobs OR food OR health", "mode": "ArtList", "format": "json", "maxrecords": max(1, int(limit))}
            request = Request(f"{GDELT_ENDPOINT}?{urlencode(params)}")
            request.add_header("User-Agent", "SignalAI/1.0")
            with urlopen(request, timeout=10) as response:  # noqa: S310 - fixed public API endpoint
                payload = json.loads(response.read().decode("utf-8"))
            articles = payload.get("articles", [])[: max(1, int(limit))]
            raw = [{"signal_name": item.get("title", "Kenya economic news"), "source": self.source_label, "location": location, "growth": "news context"} for item in articles]
            status = ProviderStatus(self.provider_name, self.provider_type, True, True, "gdelt", "Public news context loaded.")
            return ProviderResult(normalize_signals(raw, source=self.source_label, provider_type=self.provider_type, location=location), self.provider_name, self.provider_type, self.source_label, True, status)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            status = ProviderStatus(self.provider_name, self.provider_type, False, True, "gdelt", f"GDELT unavailable: {exc}")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])