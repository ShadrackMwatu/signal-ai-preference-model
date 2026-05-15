"""Kenya signal fusion engine for aggregate public intelligence."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.data_sources import fallback_sample_source
from Behavioral_Signals_AI.data_sources import google_trends_kenya, kenya_news_source, knbs_source, kilimostat_source, wfp_food_prices_source, worldbank_food_prices_source, cbk_source
from Behavioral_Signals_AI.data_sources import youtube_public_trends, reddit_public_kenya, food_price_monitor, cbk_macro_signals, knbs_indicator_source, kilimostat_agriculture_source
from Behavioral_Signals_AI.privacy import sanitize_aggregate_record
from Behavioral_Signals_AI.signal_engine.kenya_interpretation_engine import interpret_kenya_signal
from Behavioral_Signals_AI.signal_engine.signal_classifier import classify_topic
from Behavioral_Signals_AI.signal_engine.signal_memory import load_signal_memory, save_signal_memory
from Behavioral_Signals_AI.signal_engine.signal_normalizer import normalize_source_record
from Behavioral_Signals_AI.signal_engine.signal_quality import score_signal_quality
from Behavioral_Signals_AI.signal_engine.validation_engine import validate_signal
from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import adapt_signal_scores, load_cluster_memory, load_feedback, update_signal_memory
from Behavioral_Signals_AI.signal_engine.continuous_improvement import improve_after_refresh

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
        youtube_public_trends.collect,
        reddit_public_kenya.collect,
        food_price_monitor.collect,
        wfp_food_prices_source.collect,
        worldbank_food_prices_source.collect,
        kilimostat_agriculture_source.collect,
        kilimostat_source.collect,
        knbs_indicator_source.collect,
        knbs_source.collect,
        cbk_macro_signals.collect,
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
    raw_records = collect_kenya_source_records(location, limit * 2)
    records: list[dict[str, Any]] = []
    for raw in raw_records:
        normalized = normalize_source_record(raw)
        normalized["source_summary"] = raw.get("source_summary", "Aggregate public signals")
        records.append(normalized)

    quality_records: list[dict[str, Any]] = []
    for record in records:
        quality = score_signal_quality(record, records)
        record.update(quality)
        if quality.get("accepted"):
            quality_records.append(record)
    if not quality_records:
        quality_records = records[:]

    legacy_memory = load_signal_memory()
    adaptive_memory = load_cluster_memory()
    feedback = load_feedback()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in quality_records:
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
        persistence = _persistence(topic, legacy_memory)
        urgency_score = max(search_growth, price_pressure)
        multi_source = min(100.0, source_count * 34.0)
        quality_score = _avg(group, "quality_score")
        priority = (
            search_growth * 0.22
            + news_frequency * 0.16
            + price_pressure * 0.18
            + persistence * 0.13
            + urgency_score * 0.09
            + multi_source * 0.10
            + quality_score * 0.12
        )
        demand_level = _level(_avg(group, "relative_interest") * 0.45 + priority * 0.55)
        opportunity_level = _level(priority * 0.62 + multi_source * 0.23 + quality_score * 0.15)
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
            "confidence_score": round(min(96.0, 38.0 + priority * 0.36 + multi_source * 0.10 + quality_score * 0.12), 1),
            "last_updated": str(base.get("timestamp") or datetime.now(UTC).isoformat()),
            "recommended_action": "",
            "priority_score": round(priority, 2),
            "momentum": _momentum(search_growth, priority),
            "privacy_level": "aggregate_public",
            "source_reliability_score": round(_avg(group, "source_reliability_score"), 2),
            "recency_score": round(_avg(group, "recency_score"), 2),
            "category_confidence_score": round(_avg(group, "category_confidence_score"), 2),
            "multi_source_confirmation_score": round(_avg(group, "multi_source_confirmation_score"), 2),
            "quality_score": round(quality_score, 2),
            "noise_level": round(_avg(group, "noise_level"), 2),
        }
        signal.update(validate_signal(signal))
        interpretation = interpret_kenya_signal(signal)
        signal.update(interpretation)
        signal["recommended_action"] = interpretation["near_term_monitoring_recommendation"]
        signal = adapt_signal_scores(signal, adaptive_memory, feedback)
        signal["demand_level"] = _level(float(signal.get("demand_intelligence_score", priority)))
        signal["opportunity_level"] = _level(float(signal.get("opportunity_intelligence_score", priority)))
        signal["urgency"] = _urgency(float(signal.get("urgency_score", urgency_score)))
        fused.append(signal)

    filtered = [signal for signal in fused if _matches(signal, category, urgency)]
    filtered.sort(key=lambda item: (float(item.get("confidence_score", 0)), float(item.get("priority_score", 0))), reverse=True)
    filtered = filtered[:limit]
    memory_after = update_signal_memory(filtered)
    improvement = improve_after_refresh(filtered, memory_after)
    for signal in filtered:
        signal["continuous_improvement"] = improvement.get("ranking_note", "Adaptive ranking updated after refresh.")
    save_signal_memory(filtered)
    return filtered

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