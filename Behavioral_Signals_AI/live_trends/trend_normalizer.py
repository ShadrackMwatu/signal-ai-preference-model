"""Normalize public aggregate trend records into Signal's trend schema."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

PERSONAL_DATA_FIELDS = {
    "user",
    "username",
    "screen_name",
    "user_id",
    "author_id",
    "profile",
    "profile_url",
    "email",
    "phone",
    "text",
    "tweet_text",
}

CATEGORY_KEYWORDS = {
    "prices": ("price", "fuel", "inflation", "cost", "fees", "rent", "electricity"),
    "jobs": ("job", "employment", "hiring", "youth", "work"),
    "health": ("health", "hospital", "medicine", "doctor", "clinic"),
    "food_agriculture": ("food", "maize", "agri", "farm", "fertilizer", "milk"),
    "mobility_logistics": ("transport", "matatu", "traffic", "logistics", "delivery", "fuel"),
    "finance": ("credit", "loan", "bank", "lending", "mobile money", "tax", "vat"),
    "technology": ("digital", "ai", "tech", "data", "online", "app"),
    "trade": ("import", "export", "tariff", "trade", "customs"),
    "public_services": ("water", "school", "education", "county", "housing", "security"),
}


def normalize_trend_record(raw: dict[str, Any], *, platform: str, location: str, rank: int | None = None) -> dict[str, Any]:
    """Return a privacy-safe standardized trend record."""

    scrubbed = {key: value for key, value in dict(raw).items() if key not in PERSONAL_DATA_FIELDS}
    trend_name = str(
        scrubbed.get("trend_name")
        or scrubbed.get("name")
        or scrubbed.get("query")
        or scrubbed.get("title")
        or "Unavailable"
    ).strip()
    volume = _coerce_volume(
        scrubbed.get("volume")
        or scrubbed.get("tweet_volume")
        or scrubbed.get("search_volume")
        or scrubbed.get("traffic")
    )
    timestamp = str(scrubbed.get("timestamp") or scrubbed.get("fetched_at") or datetime.now(UTC).isoformat())
    category = str(scrubbed.get("category") or classify_category(trend_name))
    growth = scrubbed.get("growth_indicator") or scrubbed.get("growth") or scrubbed.get("rank_change")
    confidence = _confidence_from_rank_volume(rank or scrubbed.get("rank"), volume, bool(scrubbed.get("is_live", True)))
    relevance = _relevance_to_demand(category, volume, confidence)

    return {
        "trend_name": trend_name,
        "platform": platform,
        "source": scrubbed.get("source") or platform,
        "location": str(scrubbed.get("location") or location),
        "rank": int(rank or scrubbed.get("rank") or 1),
        "volume": volume,
        "tweet_volume": volume if platform.lower().startswith("x") else scrubbed.get("tweet_volume"),
        "growth_indicator": growth or "not available",
        "category": category,
        "timestamp": timestamp,
        "fetched_at": timestamp,
        "confidence": round(confidence, 3),
        "relevance_to_demand": round(relevance, 3),
        "possible_policy_or_business_implication": build_implication(trend_name, category, relevance),
    }


def normalize_trend_records(records: list[dict[str, Any]], *, platform: str, location: str) -> list[dict[str, Any]]:
    return [normalize_trend_record(record, platform=platform, location=location, rank=index) for index, record in enumerate(records, start=1)]


def assert_aggregate_privacy(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reject records that include obvious individual-level fields."""

    for record in records:
        present = PERSONAL_DATA_FIELDS.intersection(record.keys())
        if present:
            raise ValueError(f"Trend records must be aggregate only; found personal fields: {sorted(present)}")
    return records


def classify_category(name: str) -> str:
    lowered = name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general_public_interest"


def build_implication(trend_name: str, category: str, relevance: float) -> str:
    category_notes = {
        "prices": "may indicate price pressure, household purchasing stress, or demand for lower-cost alternatives",
        "jobs": "may indicate labour-market concern, skills demand, or youth employment opportunity",
        "health": "may indicate public-service pressure, healthcare demand, or access constraints",
        "food_agriculture": "may indicate food supply, farm-input, logistics, or household welfare pressure",
        "mobility_logistics": "may indicate transport cost, logistics bottlenecks, or delivery-market opportunity",
        "finance": "may indicate credit demand, tax concern, or household cash-flow pressure",
        "technology": "may indicate adoption momentum for digital services or productivity tools",
        "trade": "may indicate import, export, price, or competitiveness concerns",
        "public_services": "may indicate public concern over service delivery, shortages, or infrastructure gaps",
    }
    note = category_notes.get(category, "may indicate emerging public attention or market opportunity")
    strength = "high" if relevance >= 0.7 else "moderate" if relevance >= 0.45 else "early"
    return f"{trend_name} shows {strength} demand relevance and {note}."


def _coerce_volume(value: Any) -> int | None:
    if value in {None, "", "not available"}:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    cleaned = str(value).replace(",", "").replace("+", "").strip()
    suffix = 1
    if cleaned.lower().endswith("k"):
        suffix = 1000
        cleaned = cleaned[:-1]
    elif cleaned.lower().endswith("m"):
        suffix = 1000000
        cleaned = cleaned[:-1]
    try:
        return int(float(cleaned) * suffix)
    except ValueError:
        return None


def _confidence_from_rank_volume(rank: Any, volume: int | None, is_live: bool) -> float:
    try:
        rank_strength = max(0.2, 1.0 - ((int(rank or 1) - 1) / 25.0))
    except (TypeError, ValueError):
        rank_strength = 0.55
    volume_strength = 0.45 if volume is None else min(float(volume) / 250000.0, 1.0)
    live_bonus = 0.1 if is_live else -0.05
    return min(max((rank_strength * 0.48) + (volume_strength * 0.42) + live_bonus, 0.15), 0.98)


def _relevance_to_demand(category: str, volume: int | None, confidence: float) -> float:
    category_weight = 0.75 if category != "general_public_interest" else 0.5
    volume_weight = 0.45 if volume is None else min(float(volume) / 200000.0, 1.0)
    return min(max((category_weight * 0.45) + (volume_weight * 0.25) + (confidence * 0.3), 0.1), 0.98)