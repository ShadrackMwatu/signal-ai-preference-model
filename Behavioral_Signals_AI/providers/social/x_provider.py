"""X/Twitter aggregate trend provider adapter."""

from __future__ import annotations

from Behavioral_Signals_AI.live_trends.x_trends_provider import XTrendsProvider
from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals


class XAggregateProvider:
    provider_name = "x"
    provider_type = "social"
    source_label = "X"

    def __init__(self) -> None:
        self._provider = XTrendsProvider()

    def is_available(self) -> bool:
        return self._provider.is_available()

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        result = self._provider.fetch_trends(location=location, limit=limit)
        raw = [
            {
                "signal_name": record.get("trend_name"),
                "source": "X",
                "volume": record.get("volume") or record.get("tweet_volume"),
                "growth": record.get("growth_indicator"),
                "category": record.get("category"),
                "location": record.get("location", location),
                "confidence": record.get("confidence"),
                "demand_relevance": record.get("relevance_to_demand"),
            }
            for record in result.records
        ]
        status = ProviderStatus(self.provider_name, self.provider_type, bool(raw), self.is_available(), "x", result.status.message)
        return ProviderResult(normalize_signals(raw, source="X", provider_type=self.provider_type, location=location), self.provider_name, self.provider_type, self.source_label, bool(raw), status, result.warnings)