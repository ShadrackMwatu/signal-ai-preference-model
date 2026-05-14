"""Future Fintech Aggregates aggregate signal provider."""

from __future__ import annotations

import os

from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus


class FintechAggregateProvider:
    provider_name = "fintech"
    provider_type = "fintech"
    source_label = "Fintech Aggregates"

    def is_available(self) -> bool:
        return bool(os.getenv("FINTECH_AGGREGATE_API_KEY", "" ).strip())

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        status = ProviderStatus(self.provider_name, self.provider_type, False, self.is_available(), self.provider_name, "Fintech Aggregates requires a formal aggregate data integration and is not active in Phase 1.")
        return ProviderResult([], self.provider_name, self.provider_type, self.source_label, False, status, [status.message])