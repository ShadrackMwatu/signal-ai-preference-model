"""RSS public information provider placeholder."""

from __future__ import annotations

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus


class RssProvider:
    provider_name = "rss"
    provider_type = "news"
    source_label = "Public RSS"

    def is_available(self) -> bool:
        return False

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        status = ProviderStatus(self.provider_name, self.provider_type, False, False, "rss", "RSS provider is reserved for configured public feeds.")
        return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])