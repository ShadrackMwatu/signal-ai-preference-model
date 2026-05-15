"""Refresh aggregated place activity intelligence safely."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from .google_places_activity_connector import build_place_activity_profile, google_maps_available
from .mobility_signal_scorer import score_place_activity_signal
from .place_activity_cache import read_place_activity_cache, write_place_activity_cache
from .popularity_signal_engine import generate_place_activity_signal
from .privacy_guard import apply_privacy_guard

DEFAULT_QUERIES = ["supermarkets", "pharmacies", "bus stations", "hardware shops", "banks", "water points"]


def mobility_enabled() -> bool:
    return os.getenv("ENABLE_MOBILITY_INTELLIGENCE", "true").lower() not in {"0", "false", "no", "off"}


def refresh_place_activity(region: str = "Kenya", limit: int = 8) -> dict[str, Any]:
    if not mobility_enabled() or os.getenv("ALLOW_PERSONAL_LOCATION_DATA", "false").lower() == "true":
        return read_place_activity_cache()
    records: list[dict[str, Any]] = []
    if google_maps_available():
        for query in DEFAULT_QUERIES:
            try:
                records.extend(build_place_activity_profile(location_scope=region, queries=[query], limit=max(1, limit // len(DEFAULT_QUERIES))))
            except Exception:
                continue
    if not records:
        cached = read_place_activity_cache()
        if cached.get("records"):
            return cached
    safe_records = [apply_privacy_guard(record) for record in records[:limit]]
    mobility_signals = []
    for record in safe_records:
        signal = generate_place_activity_signal(record)
        signal.update(score_place_activity_signal(record))
        mobility_signals.append(signal)
    payload = {
        "last_updated": datetime.now(UTC).isoformat(),
        "region": region,
        "source_mode": os.getenv("MOBILITY_SOURCE_MODE", "google_maps_ecosystem"),
        "google_maps_available": google_maps_available(),
        "records": safe_records,
        "signals": mobility_signals,
        "privacy_level": "aggregated_place_intelligence_only",
    }
    write_place_activity_cache(payload)
    return payload


def refresh_county_activity(county: str) -> dict[str, Any]:
    return refresh_place_activity(region=county)


def refresh_global_activity() -> dict[str, Any]:
    return refresh_place_activity(region="Global")