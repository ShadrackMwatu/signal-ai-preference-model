"""Provider base types and schema normalization for aggregate public signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

STANDARD_PRIVACY_LEVEL = "aggregate_public"
PERSONAL_FIELDS = {
    "username",
    "user_id",
    "screen_name",
    "author_id",
    "profile_url",
    "email",
    "phone",
    "raw_post",
    "text",
    "message",
    "comment_text",
}


@dataclass(frozen=True)
class ProviderStatus:
    provider: str
    provider_type: str
    available: bool
    configured: bool
    mode: str
    message: str = ""


@dataclass
class ProviderResult:
    signals: list[dict[str, Any]]
    provider: str
    provider_type: str
    source_label: str
    is_live: bool
    status: ProviderStatus
    warnings: list[str] = field(default_factory=list)


class AggregateSignalProvider(Protocol):
    provider_name: str
    provider_type: str
    source_label: str

    def is_available(self) -> bool:
        """Return whether the provider can fetch live aggregate data in this runtime."""

    def fetch_signals(self, location: str = "Kenya", limit: int = 10) -> ProviderResult:
        """Fetch aggregate public signals."""


def normalize_signal(raw: dict[str, Any], *, source: str, provider_type: str, location: str = "Kenya") -> dict[str, Any]:
    """Normalize provider output to the Behavioral Signals aggregate schema."""

    safe = {key: value for key, value in dict(raw).items() if key not in PERSONAL_FIELDS}
    signal_name = str(
        safe.get("signal_name")
        or safe.get("trend_name")
        or safe.get("query")
        or safe.get("title")
        or safe.get("name")
        or "Aggregate signal"
    ).strip()
    category = str(safe.get("category") or classify_signal_category(signal_name))
    timestamp = str(safe.get("timestamp") or safe.get("fetched_at") or datetime.now(UTC).isoformat())
    volume = coerce_number(safe.get("volume") or safe.get("tweet_volume") or safe.get("search_volume") or safe.get("traffic"), None)
    confidence = coerce_percent(safe.get("confidence"), default=_confidence_from_volume(volume))
    relevance = coerce_percent(safe.get("demand_relevance") or safe.get("relevance_to_demand"), default=_category_relevance(category))

    return {
        "signal_name": signal_name,
        "source": str(safe.get("source") or source),
        "provider_type": provider_type,
        "category": category,
        "location": str(safe.get("location") or location or "Kenya"),
        "timestamp": timestamp,
        "volume": volume,
        "growth": safe.get("growth") or safe.get("growth_indicator"),
        "sentiment": safe.get("sentiment"),
        "engagement_velocity": coerce_number(safe.get("engagement_velocity"), None),
        "search_intensity": coerce_number(safe.get("search_intensity") or safe.get("search_volume") or safe.get("traffic"), volume),
        "demand_relevance": round(relevance, 3),
        "confidence": round(confidence, 3),
        "privacy_level": STANDARD_PRIVACY_LEVEL,
    }


def normalize_signals(records: list[dict[str, Any]], *, source: str, provider_type: str, location: str = "Kenya") -> list[dict[str, Any]]:
    return [normalize_signal(record, source=source, provider_type=provider_type, location=location) for record in records]


def assert_privacy_safe_signal(signal: dict[str, Any]) -> dict[str, Any]:
    found = PERSONAL_FIELDS.intersection(signal.keys())
    if found:
        raise ValueError(f"Aggregate provider output contains personal fields: {sorted(found)}")
    if signal.get("privacy_level") != STANDARD_PRIVACY_LEVEL:
        raise ValueError("Provider output must be aggregate_public.")
    return signal


def assert_privacy_safe_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [assert_privacy_safe_signal(signal) for signal in signals]


def classify_signal_category(name: str) -> str:
    lowered = name.lower()
    checks = {
        "prices": ("price", "fuel", "inflation", "cost", "fees", "rent", "electricity"),
        "jobs": ("job", "employment", "hiring", "youth", "work"),
        "health": ("health", "hospital", "clinic", "medicine", "near me"),
        "food_agriculture": ("maize", "flour", "food", "farm", "fertilizer", "milk"),
        "mobility_logistics": ("transport", "traffic", "delivery", "logistics", "fuel station"),
        "finance": ("credit", "loan", "bank", "lending", "mpesa", "tax", "vat"),
        "technology": ("smartphone", "digital", "app", "ai", "online", "data"),
        "trade": ("import", "export", "tariff", "customs", "trade"),
        "public_services": ("water", "school", "education", "county", "housing", "security"),
        "commerce": ("buy", "cheap", "discount", "jumia", "market", "product"),
    }
    for category, keywords in checks.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general_public_interest"


def coerce_number(value: Any, default: float | None) -> float | None:
    if value in {None, "", "not available"}:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace(",", "").replace("+", "").strip()
    multiplier = 1.0
    if cleaned.lower().endswith("k"):
        multiplier = 1000.0
        cleaned = cleaned[:-1]
    elif cleaned.lower().endswith("m"):
        multiplier = 1000000.0
        cleaned = cleaned[:-1]
    try:
        return float(cleaned) * multiplier
    except ValueError:
        return default


def coerce_percent(value: Any, default: float = 0.55) -> float:
    number = coerce_number(value, default)
    if number is None:
        number = default
    if number > 1:
        number = number / 100.0
    return min(max(float(number), 0.05), 0.98)


def _confidence_from_volume(volume: float | None) -> float:
    if volume is None:
        return 0.55
    return min(max(0.42 + (float(volume) / 500000.0), 0.45), 0.92)


def _category_relevance(category: str) -> float:
    if category in {"prices", "jobs", "health", "food_agriculture", "finance", "public_services"}:
        return 0.78
    if category in {"technology", "mobility_logistics", "trade", "commerce"}:
        return 0.68
    return 0.52