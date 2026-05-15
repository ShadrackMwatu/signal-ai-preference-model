"""Safe Google Maps ecosystem connector for public place metadata.

This connector does not request, infer, or store personal mobility traces. It only
uses public place metadata when GOOGLE_MAPS_API_KEY is configured.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from typing import Any

from .mobility_schema import AggregatedPlaceActivityIndicator, today_iso
from .place_classifier import classify_place
from .privacy_guard import apply_privacy_guard

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def google_maps_available() -> bool:
    return bool(os.getenv("GOOGLE_MAPS_API_KEY", "").strip())


def search_places(query: str, region: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not key:
        return []
    params = urllib.parse.urlencode({"query": f"{query} {region}", "key": key})
    data = _get_json(f"{PLACES_TEXT_SEARCH_URL}?{params}")
    return list(data.get("results", []))[:limit]


def get_place_details(place_id: str) -> dict[str, Any]:
    key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not key or not place_id:
        return {}
    fields = "place_id,name,types,rating,user_ratings_total,business_status,opening_hours,formatted_address"
    params = urllib.parse.urlencode({"place_id": place_id, "fields": fields, "key": key})
    data = _get_json(f"{PLACE_DETAILS_URL}?{params}")
    return dict(data.get("result", {}))


def classify_google_place_types(types: list[str] | None) -> str:
    return classify_place("", " ".join(types or []))


def build_place_activity_profile(region: str = "Kenya", query: str = "popular places", limit: int = 10) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for place in search_places(query, region, limit=limit):
        details = get_place_details(str(place.get("place_id", ""))) or place
        merged = {**place, **details}
        category = classify_place(str(merged.get("name", "")), list(merged.get("types", [])))
        rating_count = int(merged.get("user_ratings_total") or 0)
        rating = float(merged.get("rating") or 0)
        prominence = _place_prominence(rating, rating_count, str(merged.get("business_status", "")))
        record = AggregatedPlaceActivityIndicator(
            region=region,
            county=_county_from_region(region),
            place_name=str(merged.get("name", "Unknown place")),
            place_id=str(merged.get("place_id", "")),
            place_category=category,
            popularity_level=_level(prominence),
            activity_indicator="increasing" if prominence >= 74 else "stable" if prominence >= 38 else "decreasing",
            review_activity_level=_level(min(100.0, rating_count / 10.0)),
            estimated_activity_trend="rising" if prominence >= 74 else "stable" if prominence >= 38 else "falling",
            place_prominence=round(prominence, 2),
            date=today_iso(),
            source="google_maps_ecosystem_public_place_metadata",
            confidence=round(min(95.0, 45.0 + prominence * 0.45), 2),
        ).to_dict()
        profiles.append(apply_privacy_guard(record))
    return profiles


def _get_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def _place_prominence(rating: float, rating_count: int, business_status: str) -> float:
    status_bonus = 8.0 if business_status == "OPERATIONAL" else 0.0
    rating_score = min(100.0, max(0.0, rating / 5.0 * 45.0))
    count_score = min(47.0, rating_count / 20.0)
    return min(100.0, rating_score + count_score + status_bonus)


def _level(score: float) -> str:
    if score >= 82:
        return "very_high"
    if score >= 62:
        return "high"
    if score >= 35:
        return "moderate"
    return "low"


def _county_from_region(region: str) -> str:
    return "Kenya-wide" if str(region).lower() in {"kenya", "global", ""} else str(region)