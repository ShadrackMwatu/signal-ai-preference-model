"""Kenya signal fusion engine for aggregate public intelligence."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.data_sources import fallback_sample_source
from Behavioral_Signals_AI.data_sources import google_trends_kenya, kenya_news_source, knbs_source, kilimostat_source, wfp_food_prices_source, worldbank_food_prices_source, cbk_source
from Behavioral_Signals_AI.privacy import sanitize_aggregate_record
from Behavioral_Signals_AI.signal_engine.kenya_interpretation_engine import interpret_kenya_signal
from Behavioral_Signals_AI.signal_engine.signal_classifier import classify_topic
from Behavioral_Signals_AI.signal_engine.signal_memory import load_signal_memory, save_signal_memory
from Behavioral_Signals_AI.signal_engine.signal_normalizer import normalize_source_record

KENYA_COUNTIES = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo Marakwet", "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit", "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi", "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri", "Samburu", "Siaya", "Taita Taveta", "Tana River", "Tharaka Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot",
]

KENYA_CATEGORIES = [
    "food and agriculture", "jobs and labour market", "health", "education", "housing", "transport", "energy", "water and sanitation", "technology and digital economy", "finance and credit", "cost of living", "climate and environment", "public services", "trade and business", "security and governance", "other",
]


def detect_county(text: str) -> str:
    lower = str(text or "").lower()
    for county in KENYA_COUNTIES:
        if county.lower() in lower:
            return county
    return "Kenya-wide"


def collect_kenya_source_records(location: str = "Kenya", limit: int = 12) -> list[dict[str, Any]]:
    collectors = [
        google_trends_kenya.collect,
        kenya_news_source.collect,
        wfp_food_prices_source.collect,
        worldbank_food_prices_source.collect,
        kilimostat_source.collect,
        knbs_source.collect,
        cbk_source.collect,
    ]
    records: list[dict[str, Any]] = []
    for collector in collectors:
        try:
            records.extend(collector(location=location, limit=limit))
        except Exception:
            continue
    if not records:
        records = fallback_sample_source.collect(location=location, limit=limit)
    return [sanitize_aggregate_record(record) for record in records[: max(limit, 1)]]


def fuse_kenya_signals(location: str = "Kenya", category: str = "All", urgency: str = "All", limit: int = 10) -> list[dict[str, Any]]:
    records = [normalize_source_record(record) | {"source_summary": record.get("source_summary", "Aggregate public signals")} for record in collect_kenya_source_records(location, limit * 2)]
    memory = load_signal_memory()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[_topic_key(record.get("topic", ""))].append(record)

    fused: list[dict[str, Any]] = []
    for _, group in grouped.items():
        base = group[0]
        topic = str(base.get("topic", "Kenya signal"))
        signal_category = _kenya_category(topic, str(base.get("category", "other")))
        county = detect_county(topic)
        source_count = len({str(item.get("source_type", "aggregate_public")) for item in group})
        search_growth = _avg(group, "growth_signal")
        news_frequency = 65.0 if any("news" in str(item.get("source_type", "")) for item in group) else 42.0
        price_pressure = _price_pressure(topic, signal_category, group)
        persistence = _persistence(topic, memory)
        urgency_score = max(search_growth, price_pressure)
        multi_source = min(100.0, source_count * 34.0)
        priority = search_growth * 0.25 + news_frequency * 0.20 + price_pressure * 0.20 + persistence * 0.15 + urgency_score * 0.10 + multi_source * 0.10
        demand_level = _level(_avg(group, "relative_interest") * 0.50 + priority * 0.50)
        opportunity_level = _level(priority * 0.68 + multi_source * 0.32)
        unmet_level = _unmet_level(price_pressure, urgency_score)
        urgency_label = _urgency(urgency_score)
        source_summary = _source_summary(group)
        signal = {
            "signal_topic": topic,
            "signal_category": signal_category,
            "demand_level": demand_level,
            "opportunity_level": opportunity_level,
            "unmet_demand_likelihood": unmet_level,
            "urgency": urgency_label,
            "geographic_scope": county if county != "Kenya-wide" else (location if location not in {"Kenya", "Global"} else "Kenya-wide"),
            "source_summary": source_summary,
            "confidence_score": round(min(96.0, 42.0 + priority * 0.42 + multi_source * 0.12), 1),
            "last_updated": str(base.get("timestamp") or datetime.now(UTC).isoformat()),
            "recommended_action": "",
            "priority_score": round(priority, 2),
            "momentum": _momentum(search_growth, priority),
            "privacy_level": "aggregate_public",
        }
        interpretation = interpret_kenya_signal(signal)
        signal.update(interpretation)
        signal["recommended_action"] = interpretation["near_term_monitoring_recommendation"]
        fused.append(signal)

    filtered = [signal for signal in fused if _matches(signal, category, urgency)]
    filtered.sort(key=lambda item: float(item.get("priority_score", 0)), reverse=True)
    save_signal_memory(filtered[:limit])
    return filtered[:limit]


def _topic_key(topic: str) -> str:
    return " ".join(str(topic).lower().strip().split())


def _avg(records: list[dict[str, Any]], key: str) -> float:
    values = []
    for record in records:
        try:
            values.append(float(record.get(key, 0)))
        except Exception:
            pass
    return sum(values) / len(values) if values else 0.0


def _kenya_category(topic: str, category: str) -> str:
    mapped = classify_topic(topic, category).lower()
    aliases = {
        "technology": "technology and digital economy",
        "finance": "finance and credit",
        "prices": "cost of living",
    }
    mapped = aliases.get(mapped, mapped)
    return mapped if mapped in KENYA_CATEGORIES else (category if category in KENYA_CATEGORIES else "other")


def _price_pressure(topic: str, category: str, records: list[dict[str, Any]]) -> float:
    text = f"{topic} {category}".lower()
    base = _avg(records, "relative_interest") * 0.35 + _avg(records, "growth_signal") * 0.45
    if any(word in text for word in ["price", "prices", "flour", "fuel", "rent", "fees", "water", "shortage"]):
        base += 20
    return min(100.0, base)


def _persistence(topic: str, memory: list[dict[str, Any]]) -> float:
    key = _topic_key(topic)
    count = sum(1 for item in memory if _topic_key(item.get("signal_topic") or item.get("topic") or "") == key)
    return min(95.0, 45.0 + count * 12.5)


def _source_summary(group: list[dict[str, Any]]) -> str:
    source_types = {str(item.get("source_type", "aggregate public signal")).replace("_", " ").title() for item in group}
    if len(source_types) <= 1 and group:
        summary = str(group[0].get("source_summary") or next(iter(source_types)))
    else:
        summary = " + ".join(sorted(source_types))
    return summary.replace("Demo", "Sample")


def _level(score: float) -> str:
    if score >= 74:
        return "High"
    if score >= 50:
        return "Moderate"
    return "Low"


def _unmet_level(price_pressure: float, urgency_score: float) -> str:
    score = price_pressure * 0.55 + urgency_score * 0.45
    if score >= 74:
        return "High"
    if score >= 50:
        return "Medium"
    return "Low"


def _urgency(score: float) -> str:
    if score >= 76:
        return "High"
    if score >= 52:
        return "Medium"
    return "Low"


def _momentum(search_growth: float, priority: float) -> str:
    if search_growth >= 85 or priority >= 82:
        return "Breakout"
    if search_growth >= 62:
        return "Rising"
    if search_growth <= 35:
        return "Declining"
    return "Stable"


def _matches(signal: dict[str, Any], category: str, urgency: str) -> bool:
    if category != "All" and str(signal.get("signal_category", "")).lower() != category.lower():
        return False
    if urgency != "All" and str(signal.get("urgency", "")).lower() != urgency.lower():
        return False
    return True