"""Safe Google Maps ecosystem connector for public place metadata.

This connector does not request, infer, or store personal mobility traces. It only
uses public place metadata when GOOGLE_MAPS_API_KEY is configured.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any

from .mobility_schema import AggregatedPlaceActivityIndicator, today_iso
from .place_classifier import classify_place, demand_category_to_signal_category
from .privacy_guard import apply_privacy_guard

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DEFAULT_PLACE_QUERIES = ["supermarket", "market", "pharmacy", "hospital", "bus station", "hardware", "school", "bank", "water point"]


def google_maps_available() -> bool:
    return bool(os.getenv("GOOGLE_MAPS_API_KEY", "").strip())


def geocode_region(region: str) -> dict[str, Any]:
    key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not key:
        return {}
    params = urllib.parse.urlencode({"address": region, "key": key})
    data = _get_json(f"{GEOCODING_URL}?{params}")
    result = (data.get("results") or [{}])[0]
    return {"formatted_address": result.get("formatted_address", region), "place_id": result.get("place_id", "")}


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


def build_place_activity_profile(location_scope: str = "Kenya", limit: int = 10, queries: list[str] | None = None, **kwargs: Any) -> list[dict[str, Any]]:
    """Build safe aggregate place profiles from public Google place metadata.

    `location_scope` may be Global, Kenya, or a county/city string. `region` is
    accepted as a backward-compatible alias. If no Google Maps key is configured,
    this returns an empty list and the app continues using cached aggregate data.
    """
    region = str(kwargs.get("region") or location_scope or "Kenya")
    query_list = queries or [str(kwargs.get("query"))] if kwargs.get("query") else (queries or DEFAULT_PLACE_QUERIES)
    profiles: list[dict[str, Any]] = []
    per_query_limit = max(1, limit // max(1, len(query_list)))
    for query in query_list:
        for place in search_places(str(query), region, limit=per_query_limit):
            details = get_place_details(str(place.get("place_id", ""))) or place
            merged = {**place, **details}
            profiles.append(_profile_from_place(merged, region))
            if len(profiles) >= limit:
                return profiles
    return profiles


def _profile_from_place(place: dict[str, Any], region: str) -> dict[str, Any]:
    types = list(place.get("types", []))
    place_name = str(place.get("name", "Unknown place"))
    place_category = classify_place(place_name, types)
    demand_category = demand_category_to_signal_category(place_category)
    review_count = int(place.get("user_ratings_total") or 0)
    rating = float(place.get("rating") or 0)
    business_status = str(place.get("business_status") or "unknown")
    opening_hours_status = _opening_hours_status(place.get("opening_hours"))
    prominence = _place_prominence(rating, review_count, business_status, opening_hours_status)
    record = AggregatedPlaceActivityIndicator(
        region=region,
        county=_county_from_region(region),
        place_name=place_name,
        place_id=str(place.get("place_id", "")),
        place_category=place_category,
        demand_category=demand_category,
        rating=rating,
        review_count=review_count,
        opening_hours_status=opening_hours_status,
        business_status=business_status,
        place_prominence=round(prominence, 2),
        popularity_level=_level(prominence),
        activity_indicator="increasing" if prominence >= 74 else "stable" if prominence >= 38 else "decreasing",
        estimated_activity_trend="rising" if prominence >= 74 else "stable" if prominence >= 38 else "falling",
        source="google_maps_ecosystem_public_place_metadata",
        confidence=round(min(95.0, 45.0 + prominence * 0.45), 2),
        date=today_iso(),
    ).to_dict()
    return apply_privacy_guard(record)


def _get_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def _opening_hours_status(opening_hours: Any) -> str:
    if not isinstance(opening_hours, dict):
        return "unknown"
    if opening_hours.get("open_now") is True:
        return "open_now"
    if opening_hours.get("open_now") is False:
        return "closed_now"
    return "available"


def _place_prominence(rating: float, review_count: int, business_status: str, opening_hours_status: str = "unknown") -> float:
    status_bonus = 8.0 if business_status == "OPERATIONAL" else 0.0
    hours_bonus = 5.0 if opening_hours_status in {"open_now", "available"} else 0.0
    rating_score = min(100.0, max(0.0, rating / 5.0 * 42.0))
    count_score = min(45.0, review_count / 20.0)
    return min(100.0, rating_score + count_score + status_bonus + hours_bonus)


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