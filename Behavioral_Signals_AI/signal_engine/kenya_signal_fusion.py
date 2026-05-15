"""Kenya signal fusion engine for aggregate public intelligence."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.data_sources import cbk_source, fallback_sample_source, google_trends_kenya, kenya_news_source, kilimostat_source, knbs_source, wfp_food_prices_source, worldbank_food_prices_source
from Behavioral_Signals_AI.data_sources import cbk_macro_signals, food_price_monitor, kilimostat_agriculture_source, knbs_indicator_source, reddit_public_kenya, youtube_public_trends
from Behavioral_Signals_AI.geography.county_matcher import detect_county_from_text
from Behavioral_Signals_AI.llm.signal_interpreter import interpret_signal_with_llm
from Behavioral_Signals_AI.mobility_intelligence.place_activity_refresh import refresh_place_activity
from Behavioral_Signals_AI.mobility_intelligence.signal_fusion import fuse_mobility_with_live_signals
from Behavioral_Signals_AI.privacy import sanitize_aggregate_record
from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import adapt_signal_scores, load_cluster_memory, load_feedback, update_signal_memory
from Behavioral_Signals_AI.signal_engine.behavioral_learning_engine import update_behavioral_learning
from Behavioral_Signals_AI.signal_engine.continuous_improvement import improve_after_refresh
from Behavioral_Signals_AI.signal_engine.daily_learning_engine import summarize_daily_signals
from Behavioral_Signals_AI.signal_engine.early_warning_engine import classify_early_warning
from Behavioral_Signals_AI.signal_engine.geospatial_learning import update_geospatial_learning
from Behavioral_Signals_AI.signal_engine.historical_adaptation_engine import apply_historical_adaptation
from Behavioral_Signals_AI.signal_engine.historical_forecasting_engine import add_historical_forecast, persist_forecasts
from Behavioral_Signals_AI.signal_engine.historical_memory import initialize_history_stores
from Behavioral_Signals_AI.signal_engine.kenya_context_engine import map_kenya_context
from Behavioral_Signals_AI.signal_engine.kenya_interpretation_engine import interpret_kenya_signal
from Behavioral_Signals_AI.signal_engine.monthly_learning_engine import summarize_monthly_patterns
from Behavioral_Signals_AI.signal_engine.outcome_learning_engine import apply_outcome_learning
from Behavioral_Signals_AI.signal_engine.predictive_signal_engine import predict_signal_evolution
from Behavioral_Signals_AI.signal_engine.semantic_intelligence import cluster_related_records, detect_latent_themes
from Behavioral_Signals_AI.signal_engine.signal_classifier import classify_topic
from Behavioral_Signals_AI.signal_engine.signal_memory import load_signal_memory, save_signal_memory
from Behavioral_Signals_AI.signal_engine.signal_normalizer import normalize_source_record
from Behavioral_Signals_AI.signal_engine.signal_quality import score_signal_quality
from Behavioral_Signals_AI.signal_engine.signal_relationships import detect_signal_relationships, related_signals_for_topic, relationship_summary
from Behavioral_Signals_AI.signal_engine.source_learning import update_source_learning
from Behavioral_Signals_AI.signal_engine.validation_engine import validate_signal
from Behavioral_Signals_AI.signal_engine.yearly_learning_engine import summarize_yearly_patterns

KENYA_COUNTIES = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo Marakwet", "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit", "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi", "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri", "Samburu", "Siaya", "Taita Taveta", "Tana River", "Tharaka Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot",
]

KENYA_CATEGORIES = [
    "food and agriculture", "jobs and labour market", "health", "education", "housing", "transport", "energy", "water and sanitation", "technology and digital economy", "finance and credit", "cost of living", "climate and environment", "public services", "trade and business", "security and governance", "other",
]


def detect_county(text: str) -> str:
    return detect_county_from_text(text).get("geographic_scope", "Kenya-wide")


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
    initialize_history_stores()
    raw_records = collect_kenya_source_records(location, limit * 2)
    records = _normalize_records(raw_records)
    quality_records = _quality_filter(records)
    if not quality_records:
        quality_records = records[:]

    legacy_memory = load_signal_memory()
    adaptive_memory = load_cluster_memory()
    feedback = load_feedback()
    grouped = cluster_related_records(quality_records)

    fused: list[dict[str, Any]] = []
    for semantic_topic, group in grouped.items():
        if not group:
            continue
        signal = _fuse_group(semantic_topic, group, legacy_memory)
        signal = update_behavioral_learning(signal, group)
        signal.update(validate_signal(signal))
        signal.update(interpret_kenya_signal(signal))
        signal["recommended_action"] = signal.get("near_term_monitoring_recommendation") or signal.get("recommended_action") or "Monitor and validate with additional aggregate data."
        signal = adapt_signal_scores(signal, adaptive_memory, feedback)
        signal["demand_level"] = _level(float(signal.get("demand_intelligence_score", signal.get("priority_score", 50))))
        signal["opportunity_level"] = _level(float(signal.get("opportunity_intelligence_score", signal.get("priority_score", 50))))
        signal["urgency"] = _urgency(float(signal.get("urgency_score", signal.get("priority_score", 50))))
        fused.append(signal)

    graph = detect_signal_relationships(fused)
    graph_summary = relationship_summary(graph)
    for index, signal in enumerate(fused):
        related = related_signals_for_topic(str(signal.get("signal_topic", "")), fused, graph)
        signal["related_signal_count"] = len(related)
        signal["relationship_summary"] = graph_summary
        signal.update(predict_signal_evolution(signal, adaptive_memory, related))
        signal.update(map_kenya_context(signal))
        signal.update(classify_early_warning(signal, related))
        signal = apply_historical_adaptation(signal)
        signal = update_behavioral_learning(signal, [], count_appearance=False)
        signal = add_historical_forecast(signal)
        signal = apply_outcome_learning(signal)
        signal.update(_llm_interpretation_fields(signal))
        signal = update_geospatial_learning(signal)
        signal["confidence_reasoning"] = _confidence_reasoning(signal, related)
        signal["demand_level"] = _level(float(signal.get("demand_intelligence_score", signal.get("priority_score", 50))))
        signal["opportunity_level"] = _level(float(signal.get("opportunity_intelligence_score", signal.get("priority_score", 50))))
        fused[index] = signal

    fused = _apply_mobility_reinforcement(fused, location)
    filtered = [signal for signal in fused if _matches(signal, category, urgency)]
    filtered.sort(key=lambda item: (float(item.get("confidence_score", 0)), float(item.get("priority_score", 0))), reverse=True)
    filtered = filtered[:limit]

    memory_after = update_signal_memory(filtered)
    daily_summary = summarize_daily_signals(filtered)
    monthly_summary = summarize_monthly_patterns()
    yearly_summary = summarize_yearly_patterns()
    forecast_memory = persist_forecasts(filtered)
    improvement = improve_after_refresh(filtered, memory_after)
    source_learning = update_source_learning(filtered)
    for signal in filtered:
        signal["continuous_improvement"] = improvement.get("ranking_note", "Adaptive ranking updated after refresh.")
        signal["source_learning_status"] = "updated" if source_learning.get("last_updated") else "pending"
        signal["historical_learning_status"] = "updated" if daily_summary.get("generated_at") else "pending"
        signal["monthly_learning_status"] = "updated" if monthly_summary.get("generated_at") else "pending"
        signal["yearly_learning_status"] = "updated" if yearly_summary.get("generated_at") else "pending"
        signal["forecast_memory_status"] = "updated" if forecast_memory.get("last_updated") else "pending"
    save_signal_memory(filtered)
    return filtered



def _apply_mobility_reinforcement(signals: list[dict[str, Any]], location: str) -> list[dict[str, Any]]:
    try:
        activity_payload = refresh_place_activity(region=location, limit=8)
        mobility_signals = list(activity_payload.get("signals", []))
        return fuse_mobility_with_live_signals(signals, mobility_signals)
    except Exception:
        return signals

def _llm_interpretation_fields(signal: dict[str, Any]) -> dict[str, Any]:
    try:
        interpretation = interpret_signal_with_llm(signal)
    except Exception as exc:
        interpretation = {
            "plain_language_meaning": signal.get("probable_meaning", "Aggregate signal interpretation is active."),
            "economic_interpretation": signal.get("economic_or_social_pressure", "Aggregate evidence is still developing."),
            "opportunity_interpretation": signal.get("business_opportunity", "Monitor and validate the opportunity."),
            "policy_implication": signal.get("policy_implication", "Use aggregate monitoring for policy validation."),
            "recommended_action": signal.get("recommended_action", "Monitor persistence and source agreement."),
            "risk_note": f"LLM interpretation failed safely and rule-based interpretation was retained: {exc}",
            "llm_mode": "rule_based_fallback",
        }
    return {
        "plain_language_meaning": interpretation.get("plain_language_meaning", ""),
        "economic_interpretation": interpretation.get("economic_interpretation", ""),
        "opportunity_interpretation": interpretation.get("opportunity_interpretation", signal.get("opportunity_interpretation", "")),
        "policy_implication": interpretation.get("policy_implication", signal.get("policy_implication", "")),
        "recommended_action": interpretation.get("recommended_action") or signal.get("recommended_action") or "Monitor persistence and source agreement.",
        "risk_note": interpretation.get("risk_note", "Interpret only as aggregate intelligence."),
        "llm_mode": interpretation.get("llm_mode", "rule_based_fallback"),
        "llm_input_privacy": interpretation.get("llm_input_privacy", "aggregate_sanitized"),
        "llm_warning": interpretation.get("llm_warning", ""),
        "interpretation": interpretation.get("plain_language_meaning") or signal.get("interpretation", ""),
        "business_opportunity": interpretation.get("opportunity_interpretation") or signal.get("business_opportunity", ""),
    }

def _normalize_records(raw_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for raw in raw_records:
        normalized = normalize_source_record(raw)
        normalized["source_summary"] = raw.get("source_summary", "Aggregate public signals")
        records.append(normalized)
    return records


def _quality_filter(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    quality_records: list[dict[str, Any]] = []
    for record in records:
        quality = score_signal_quality(record, records)
        record.update(quality)
        if quality.get("accepted"):
            quality_records.append(record)
    return quality_records


def _fuse_group(semantic_topic: str, group: list[dict[str, Any]], legacy_memory: list[dict[str, Any]]) -> dict[str, Any]:
    base = group[0]
    source_topics = sorted({str(item.get("topic", "Kenya signal")) for item in group if item.get("topic")})
    topic_text = " ".join(source_topics) or semantic_topic
    signal_category = _kenya_category(topic_text, str(base.get("category", "other")))
    county_info = detect_county_from_text(topic_text)
    county = county_info.get("geographic_scope", "Kenya-wide")
    source_count = len({str(item.get("source_type", "aggregate_public")) for item in group})
    search_growth = _avg(group, "growth_signal")
    news_frequency = 65.0 if any("news" in str(item.get("source_type", "")) for item in group) else 42.0
    price_pressure = _price_pressure(topic_text, signal_category, group)
    persistence = _persistence(semantic_topic, legacy_memory)
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
    source_summary = _source_summary(group)
    return {
        "signal_topic": semantic_topic or str(base.get("topic", "Kenya signal")),
        "source_topics": source_topics[:8],
        "semantic_cluster": semantic_topic,
        "latent_themes": detect_latent_themes(group),
        "signal_category": signal_category,
        "demand_level": _level(_avg(group, "relative_interest") * 0.45 + priority * 0.55),
        "opportunity_level": _level(priority * 0.62 + multi_source * 0.23 + quality_score * 0.15),
        "unmet_demand_likelihood": _unmet_level(price_pressure, urgency_score),
        "urgency": _urgency(urgency_score),
        "geographic_scope": county,
        "county_name": county_info.get("county_name", "Kenya-wide"),
        "county_code": county_info.get("county_code", ""),
        "spread_risk": "Moderate" if county != "Kenya-wide" else "Low",
        "forecast_direction": _momentum(search_growth, priority).replace("Breakout", "Rising"),
        "geospatial_insight": f"{county} aggregate evidence is being monitored for localized demand, stress, or opportunity.",
        "ml_rank_score": round(priority, 2),
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
        "multi_source_confirmation_score": round(max(multi_source, _avg(group, "multi_source_confirmation_score")), 2),
        "quality_score": round(quality_score, 2),
        "noise_level": round(_avg(group, "noise_level"), 2),
    }


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
    if any(word in text for word in ["price", "prices", "flour", "fuel", "rent", "fees", "water", "shortage", "unga", "drought"]):
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


def _confidence_reasoning(signal: dict[str, Any], related: list[dict[str, Any]]) -> str:
    reasons: list[str] = []
    if signal.get("persistence_badge") == "Persistent":
        reasons.append("the signal has appeared repeatedly in adaptive memory")
    if float(signal.get("multi_source_confirmation_score", 0)) >= 65:
        reasons.append("it is supported by multiple aggregate source types")
    if related:
        reasons.append("related economic pressure signals are also present")
    if signal.get("validation_status") == "validated":
        reasons.append("it aligns with trusted reference signal classes")
    if signal.get("predicted_direction") == "rising" or signal.get("forecast_direction") == "Rising":
        reasons.append("current and historical evidence suggest a rising near-term pattern")
    if signal.get("historical_pattern_match") and signal.get("historical_pattern_match") != "No close historical pattern yet":
        reasons.append("similar historical patterns were found")
    if float(signal.get("behavioral_intelligence_score", 0)) >= 65:
        reasons.append("repeated collective behavior raised the behavioral intelligence score")
    if signal.get("outcome_learning_status") == "historically_confirmed":
        reasons.append("similar past signals were confirmed by later aggregate outcomes")
    elif signal.get("outcome_learning_status") == "historically_weak":
        reasons.append("similar past signals were not consistently confirmed, so confidence is conservative")
    if not reasons:
        reasons.append("current aggregate evidence is active but still developing")
    return "Confidence adjusted because " + "; ".join(reasons) + "."

