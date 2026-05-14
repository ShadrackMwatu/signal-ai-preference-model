"""Provider health checks without exposing credentials."""

from __future__ import annotations

from typing import Any


def summarize_provider_health(providers: list[Any]) -> list[dict[str, Any]]:
    rows = []
    for provider in providers:
        rows.append(
            {
                "provider": getattr(provider, "provider_name", "unknown"),
                "provider_type": getattr(provider, "provider_type", "unknown"),
                "available": bool(provider.is_available()),
                "source_label": getattr(provider, "source_label", "unknown"),
            }
        )
    return rows