"""Signal quality scoring for aggregate Kenya behavioral-economic signals."""

from __future__ import annotations

from datetime import UTC, datetime
from difflib import SequenceMatcher
from typing import Any

SOURCE_RELIABILITY = {
    "official_statistics": 0.95,
    "food_price_data": 0.9,
    "macro_indicator": 0.88,
    "search_trend": 0.78,
    "news_public": 0.72,
    "social_public": 0.62,
    "aggregate_public": 0.58,
}


def score_signal_quality(record: dict[str, Any], peer_records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    peers = peer_records or []
    topic = str(record.get("topic") or record.get("signal_topic") or "")
    category = str(record.get("category") or record.get("signal_category") or "other")
    source_type = str(record.get("source_type") or "aggregate_public")
    source_reliability = SOURCE_RELIABILITY.get(source_type, 0.58) * 100
    recency = _recency_score(record.get("timestamp") or record.get("last_updated"))
    kenya_relevance = _kenya_relevance(topic, record)
    county_relevance = 75 if str(record.get("location", "")).lower() not in {"", "kenya", "global"} else 55
    duplication = _duplication_score(topic, peers)
    noise = _noise_score(topic)
    clarity = _language_clarity(topic)
    category_confidence = 80 if category and category != "other" else 52
    confirmation = _multi_source_confirmation(topic, peers)
    quality_score = (
        source_reliability * 0.18
        + recency * 0.14
        + kenya_relevance * 0.14
        + county_relevance * 0.08
        + duplication * 0.08
        + (100 - noise) * 0.12
        + clarity * 0.10
        + category_confidence * 0.12
        + confirmation * 0.14
    )
    return {
        "quality_score": round(max(0, min(100, quality_score)), 2),
        "source_reliability_score": round(source_reliability, 2),
        "recency_score": round(recency, 2),
        "kenya_relevance_score": round(kenya_relevance, 2),
        "county_relevance_score": round(county_relevance, 2),
        "duplication_score": round(duplication, 2),
        "noise_level": round(noise, 2),
        "language_clarity_score": round(clarity, 2),
        "category_confidence_score": round(category_confidence, 2),
        "multi_source_confirmation_score": round(confirmation, 2),
        "accepted": quality_score >= 42 and noise < 82 and bool(topic.strip()),
    }


def _recency_score(timestamp: Any) -> float:
    try:
        value = str(timestamp).replace("Z", "+00:00")
        observed = datetime.fromisoformat(value)
        if observed.tzinfo is None:
            observed = observed.replace(tzinfo=UTC)
        hours = max(0, (datetime.now(UTC) - observed).total_seconds() / 3600)
        return max(35, 100 - min(hours, 72) * 0.9)
    except Exception:
        return 65


def _kenya_relevance(topic: str, record: dict[str, Any]) -> float:
    text = f"{topic} {record.get('location', '')}".lower()
    kenya_terms = ["kenya", "nairobi", "mombasa", "kisumu", "nakuru", "kiambu", "makueni", "turkana", "garissa"]
    return 92 if any(term in text for term in kenya_terms) else 72


def _duplication_score(topic: str, peers: list[dict[str, Any]]) -> float:
    if not peers:
        return 50
    similarities = [SequenceMatcher(None, topic.lower(), str(peer.get("topic") or peer.get("signal_topic") or "").lower()).ratio() for peer in peers]
    near_matches = sum(1 for score in similarities if score > 0.72)
    return min(95, 45 + near_matches * 18)


def _noise_score(topic: str) -> float:
    text = topic.strip()
    if len(text) < 4:
        return 90
    noisy = sum(1 for char in text if not (char.isalnum() or char.isspace() or char in "-'&/"))
    return min(100, noisy * 12 + (20 if len(text.split()) == 1 else 0))


def _language_clarity(topic: str) -> float:
    words = [word for word in topic.split() if word]
    if len(words) >= 2:
        return 82
    if len(words) == 1 and len(words[0]) >= 5:
        return 62
    return 35


def _multi_source_confirmation(topic: str, peers: list[dict[str, Any]]) -> float:
    sources = {str(peer.get("source_type") or peer.get("source") or "aggregate_public") for peer in peers if SequenceMatcher(None, topic.lower(), str(peer.get("topic") or peer.get("signal_topic") or "").lower()).ratio() > 0.72}
    return min(100, max(35, len(sources) * 35))