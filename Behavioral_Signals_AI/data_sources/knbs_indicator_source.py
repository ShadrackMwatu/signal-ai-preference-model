"""KNBS indicator source alias for official statistics validation."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.data_sources import knbs_source


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    return knbs_source.collect(location=location, limit=limit)