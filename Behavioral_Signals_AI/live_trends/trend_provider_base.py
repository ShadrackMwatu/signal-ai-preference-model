"""Provider interface for public aggregate trend feeds."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class TrendProviderStatus:
    """Runtime status for a trend provider without exposing credentials."""

    provider: str
    available: bool
    mode: str
    message: str = ""


@dataclass
class TrendProviderResult:
    """Standard container returned by trend providers."""

    records: list[dict[str, Any]]
    provider: str
    source_label: str
    is_live: bool
    status: TrendProviderStatus
    warnings: list[str] = field(default_factory=list)


class TrendProvider(Protocol):
    """Protocol implemented by all live trend providers."""

    provider_name: str

    def is_available(self) -> bool:
        """Return whether the provider has enough configuration to call a live API."""

    def fetch_trends(self, location: str = "Kenya", limit: int = 10) -> TrendProviderResult:
        """Fetch public aggregate trends for the requested location."""