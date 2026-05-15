"""Food price aggregate monitor combining configured public food-price sources."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.data_sources import wfp_food_prices_source, worldbank_food_prices_source


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for source in (wfp_food_prices_source, worldbank_food_prices_source):
        try:
            records.extend(source.collect(location=location, limit=limit))
        except Exception:
            continue
    return records[:limit]