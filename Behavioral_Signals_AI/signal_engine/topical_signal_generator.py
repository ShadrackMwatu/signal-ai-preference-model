"""Generate UI-ready topical demand signals from aggregate public data."""

from __future__ import annotations

from html import escape
from typing import Any

from Behavioral_Signals_AI.privacy import PRIVACY_NOTE, sanitize_aggregate_record
from Behavioral_Signals_AI.signal_engine.adaptive_learning import persistence_for_topic, source_confirmation_for_topic
from Behavioral_Signals_AI.signal_engine.demand_inference import infer_topical_signal
from Behavioral_Signals_AI.signal_engine.signal_classifier import classify_topic
from Behavioral_Signals_AI.signal_engine.signal_collector import collect_aggregate_signals
from Behavioral_Signals_AI.signal_engine.signal_memory import load_signal_memory, save_signal_memory
from Behavioral_Signals_AI.signal_engine.signal_normalizer import normalize_source_record

FILTER_ALL = "All"


def generate_topical_signals(
    location: str = "Kenya",
    category: str = FILTER_ALL,
    demand_level: str = FILTER_ALL,
    urgency: str = FILTER_ALL,
    limit: int = 8,
) -> list[dict[str, Any]]:
    raw_records = collect_aggregate_signals(location=location, limit=limit)
    memory = load_signal_memory()
    normalized = [normalize_source_record(sanitize_aggregate_record(record)) for record in raw_records]
    signals: list[dict[str, Any]] = []
    for record in normalized:
        signal_category = classify_topic(record.get("topic", ""), record.get("category"))
        persistence = persistence_for_topic(record.get("topic", ""), memory)
        confirmations = source_confirmation_for_topic(record.get("topic", ""), normalized)
        signal = infer_topical_signal(record, signal_category, persistence, confirmations)
        signals.append(signal)

    signals.sort(key=lambda item: (float(item.get("confidence_score", 0)), float(item.get("opportunity_score", 0))), reverse=True)
    filtered = [_matches_filters(signal, location, category, demand_level, urgency) for signal in signals]
    output = [signal for signal, keep in zip(signals, filtered) if keep]
    save_signal_memory(output[:limit])
    return output[:limit]


def get_topical_signals_for_ui(
    location: str = "Kenya",
    category: str = FILTER_ALL,
    demand_level: str = FILTER_ALL,
    urgency: str = FILTER_ALL,
) -> tuple[str, str]:
    signals = generate_topical_signals(location, category, demand_level, urgency)
    return render_signal_feed(signals), build_signal_interpretation(signals)


def render_signal_feed(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return "<div class='signal-feed-container'><div class='signal-card'>No aggregate topical signals available yet.</div></div>"
    cards = "".join(_render_signal_card(signal) for signal in signals)
    return (
        "<div class='signal-feed-container'>"
        "<div class='signal-feed-inner'>"
        f"{cards}{cards}"
        "</div>"
        "</div>"
    )


def build_signal_interpretation(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return f"### Signal Interpretation & Opportunity\n\nNo current aggregate signal has passed the filters.\n\n**Privacy note:** {PRIVACY_NOTE}"
    top = signals[0]
    affected = ", ".join(sorted({str(signal.get("signal_category", "other")) for signal in signals[:4]}))
    return (
        "### Signal Interpretation & Opportunity\n\n"
        f"The strongest current signal is **{top['signal_topic']}**, a **{top['signal_category']}** signal with **{top['demand_level']}** demand and **{top['opportunity_level']}** opportunity. "
        f"It appears to reflect { _signal_type(top) } and is most relevant at **{top['geographic_scope']}** scope. "
        f"Affected sectors include **{affected}**. Recommended near-term action: {top['recommended_action']}\n\n"
        f"**Privacy note:** {PRIVACY_NOTE}"
    )


def _matches_filters(signal: dict[str, Any], location: str, category: str, demand_level: str, urgency: str) -> bool:
    if location and location != FILTER_ALL and location.lower() not in str(signal.get("geographic_scope", "")).lower():
        if location.lower() != "kenya":
            return False
    if category != FILTER_ALL and category.lower() != str(signal.get("signal_category", "")).lower():
        return False
    if demand_level != FILTER_ALL and demand_level.lower() != str(signal.get("demand_level", "")).lower():
        return False
    if urgency != FILTER_ALL and urgency.lower() != str(signal.get("urgency", "")).lower():
        return False
    return True


def _render_signal_card(signal: dict[str, Any]) -> str:
    topic = escape(str(signal.get("signal_topic", "Signal")))
    category = escape(str(signal.get("signal_category", "other")))
    demand = escape(str(signal.get("demand_level", "Moderate")))
    opportunity = escape(str(signal.get("opportunity_level", "Moderate")))
    unmet = escape(str(signal.get("unmet_demand_likelihood", "Medium")))
    urgency = escape(str(signal.get("urgency", "Medium")))
    scope = escape(str(signal.get("geographic_scope", "Kenya-wide")))
    confidence = escape(str(signal.get("confidence_score", 0)))
    updated = escape(str(signal.get("last_updated", "")))
    action = escape(str(signal.get("recommended_action", "Monitor and validate the signal.")))
    return (
        "<article class='signal-card'>"
        f"<div class='signal-card-topic'>{topic}</div>"
        f"<div class='signal-card-category'>{category}</div>"
        "<div class='signal-card-grid'>"
        f"<span><strong>Demand</strong>{demand}</span>"
        f"<span><strong>Opportunity</strong>{opportunity}</span>"
        f"<span><strong>Unmet need</strong>{unmet}</span>"
        f"<span><strong>Urgency</strong>{urgency}</span>"
        f"<span><strong>Scope</strong>{scope}</span>"
        f"<span><strong>Confidence</strong>{confidence}%</span>"
        "</div>"
        f"<p>{action}</p>"
        f"<div class='signal-card-time'>Last updated: {updated}</div>"
        "</article>"
    )


def _signal_type(signal: dict[str, Any]) -> str:
    category = str(signal.get("signal_category", "")).lower()
    unmet = str(signal.get("unmet_demand_likelihood", "")).lower()
    urgency = str(signal.get("urgency", "")).lower()
    if "food" in category or "energy" in category:
        return "affordability pressure and market demand"
    if "health" in category or "public" in category:
        return "a service gap and policy concern"
    if "technology" in category or "finance" in category:
        return "an investment opportunity and emerging consumption shift"
    if unmet == "high" or urgency == "high":
        return "unmet demand and near-term pressure"
    return "market demand and opportunity formation"