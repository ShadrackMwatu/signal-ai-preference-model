"""Future Instagram aggregate signal provider."""

from __future__ import annotations

import os

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus


class InstagramAggregateProvider:
    provider_name = "instagram"
    provider_type = "social"
    source_label = "Instagram"

    def is_available(self) -> bool:
        return bool(os.getenv("INSTAGRAM_ACCESS_TOKEN", "" ).strip())

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        status = ProviderStatus(self.provider_name, self.provider_type, False, self.is_available(), self.provider_name, "Instagram provider is reserved for future aggregate API integration.")
        return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])