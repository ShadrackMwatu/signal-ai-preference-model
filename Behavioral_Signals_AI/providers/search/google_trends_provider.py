"""Google Trends style aggregate search signal provider."""

from __future__ import annotations

import os

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals
from Behavioral_Signals_AI.providers.search.serpapi_provider import SerpApiSearchProvider
from Behavioral_Signals_AI.providers.search.pytrends_provider import PytrendsSearchProvider


class GoogleTrendsSearchProvider:
    provider_name = "google_trends"
    provider_type = "search"
    source_label = "Google Trends"

    def is_available(self) -> bool:
        return bool(os.getenv("GOOGLE_TRENDS_API_KEY", "").strip() or os.getenv("SERPAPI_API_KEY", "").strip()) or PytrendsSearchProvider().is_available()

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        if os.getenv("SERPAPI_API_KEY", "").strip() or os.getenv("GOOGLE_TRENDS_API_KEY", "").strip():
            return SerpApiSearchProvider().fetch_signals(location=location, limit=limit)
        if PytrendsSearchProvider().is_available():
            return PytrendsSearchProvider().fetch_signals(location=location, limit=limit)
        status = ProviderStatus(self.provider_name, self.provider_type, False, False, "google", "Google Trends credentials or optional pytrends are unavailable.")
        return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])