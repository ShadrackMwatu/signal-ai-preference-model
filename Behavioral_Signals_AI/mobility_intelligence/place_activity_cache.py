"""Safe cache for aggregated place activity intelligence."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

DEFAULT_CACHE = {"last_updated": None, "region": "Kenya", "records": [], "privacy_level": "aggregated_place_intelligence_only"}


def cache_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return Path(os.getenv("SIGNAL_PLACE_ACTIVITY_CACHE", "Behavioral_Signals_AI/outputs/place_activity_cache.json"))


def read_place_activity_cache(path: str | Path | None = None) -> dict[str, Any]:
    payload = read_json(cache_path(path), DEFAULT_CACHE.copy())
    return payload if isinstance(payload, dict) else DEFAULT_CACHE.copy()


def write_place_activity_cache(payload: dict[str, Any], path: str | Path | None = None) -> dict[str, Any]:
    payload = dict(payload)
    payload["privacy_level"] = "aggregated_place_intelligence_only"
    return write_json(cache_path(path), payload)