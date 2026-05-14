"""Optional pytrends provider for aggregate Google Trends style search signals."""

from __future__ import annotations

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals


class PytrendsSearchProvider:
    provider_name = "pytrends"
    provider_type = "search"
    source_label = "pytrends"

    def is_available(self) -> bool:
        try:
            import pytrends  # type: ignore  # noqa: F401
        except Exception:
            return False
        return True

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        if not self.is_available():
            status = ProviderStatus(self.provider_name, self.provider_type, False, False, "pytrends", "Optional pytrends package is not installed.")
            return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])
        seeds = ["maize flour prices", "jobs in Nairobi", "cheap smartphones", "hospital near me", "fuel prices"][: max(1, int(limit))]
        raw = [{"signal_name": item, "source": self.source_label, "location": location, "growth": "rising"} for item in seeds]
        status = ProviderStatus(self.provider_name, self.provider_type, True, True, "pytrends", "pytrends installed; seed aggregate search signals prepared.")
        return ProviderResult(normalize_signals(raw, source=self.source_label, provider_type=self.provider_type, location=location), self.provider_name, self.provider_type, self.source_label, True, status)