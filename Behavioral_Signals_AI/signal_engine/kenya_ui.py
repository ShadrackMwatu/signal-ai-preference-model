"""UI renderer for Kenya live aggregate signals."""

from __future__ import annotations

from html import escape
from typing import Any

from Behavioral_Signals_AI.privacy import PRIVACY_NOTE
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals

MOMENTUM_BADGES = {
    "Rising": "Rising",
    "Stable": "Stable",
    "Declining": "Declining",
    "Breakout": "Breakout",
}


def get_kenya_live_signals_for_ui(location_filter: str = "Kenya", category_filter: str = "All", urgency_filter: str = "All") -> tuple[str, str, str, str]:
    """Render the live feed from processed cache only.

    Heavy source collection is handled by background_signal_service on its own poll
    interval. The Gradio timer can safely call this every second because it only
    reads latest_live_signals.json and renders processed cards.
    """
    payload = get_cached_or_fallback_signals()
    signals = _filter_signals(list(payload.get("signals", [])), location_filter or "Kenya", category_filter or "All", urgency_filter or "All")
    if not signals:
        signals = list(payload.get("signals", []))
    if not signals:
        signals = [_friendly_empty_signal()]
    last_updated = str(payload.get("last_updated") or signals[0].get("last_updated") or "recently")
    return (
        render_live_signal_feed(signals, last_updated),
        render_emerging_signals(signals),
        render_strategic_interpretation(signals),
        render_historical_learning_insight(signals),
    )


def render_live_signal_feed(signals: list[dict[str, Any]], last_updated: str = "recently") -> str:
    safe_signals = signals or [_friendly_empty_signal()]
    repeated_signals = _repeat_for_continuous_loop(safe_signals)
    cards = "".join(_card(signal) for signal in repeated_signals)
    if not cards.strip():
        cards = _card(_friendly_empty_signal())
    loop_cards = cards + cards
    status = escape(str(last_updated or "recently"))
    return (
        f"<div class='signal-feed-status'>Live Kenya signal stream &middot; Last updated: {status}</div>"
        f"<div class='signal-feed-container'><div class='signal-feed-inner'>{loop_cards}</div></div>"
    )


def render_emerging_signals(signals: list[dict[str, Any]]) -> str:
    safe_signals = signals or [_friendly_empty_signal()]
    selected = [signal for signal in safe_signals if signal.get("momentum") in {"Rising", "Breakout"} or signal.get("urgency") == "High" or signal.get("early_warning_labels")][:4]
    if not selected:
        selected = safe_signals[:3]
    items = "".join(
        f"<li><strong>{escape(str(signal.get('signal_topic')))}</strong>: {escape(str(signal.get('momentum', 'Stable')))} momentum, {escape(str(signal.get('urgency', 'Medium')))} urgency, forecast {escape(str(signal.get('forecast_direction') or signal.get('predicted_direction', 'stable')))}, detected from {escape(str(signal.get('source_summary', 'Aggregate public sources')))}.</li>"
        for signal in selected
    )
    if not items:
        items = "<li>Kenya aggregate signal monitoring is active.</li>"
    return "<div class='signal-emerging'><h3>Emerging Kenya Signals</h3><ul>" + items + "</ul></div>"


def render_strategic_interpretation(signals: list[dict[str, Any]]) -> str:
    safe_signals = signals or [_friendly_empty_signal()]
    top = safe_signals[0]
    sectors = ", ".join(sorted({str(signal.get("signal_category", "other")) for signal in safe_signals[:5]})) or "Kenya aggregate demand"
    context_lines = [
        f"**Macro implications:** {top.get('macro_implications', 'Aggregate evidence is still developing.')}",
        f"**Sector implications:** {top.get('sector_implications', 'Relevant sectors should monitor the signal as evidence accumulates.')}",
        f"**County implications:** {top.get('county_implications', 'Current evidence is Kenya-wide unless county evidence strengthens.')}",
        f"**Business opportunity:** {top.get('business_opportunity', 'Monitor demand pockets and test targeted responses using aggregate evidence.')}",
        f"**Policy opportunity:** {top.get('policy_opportunity', 'Use this as an early signal for policy monitoring and validation.')}",
        f"**Risk outlook:** {top.get('risk_outlook', 'Risk outlook is stable under current aggregate evidence.')}",
        f"**Monitoring recommendation:** {top.get('monitoring_recommendation', top.get('recommended_action', 'Monitor persistence and source agreement.'))}",
    ]
    return (
        "### Signal Interpretation & Opportunity\n\n"
        f"**Top signal:** {top.get('signal_topic', 'Kenya aggregate signal')} ({top.get('signal_category', 'other')}). {top.get('interpretation', 'Signal monitoring is active and awaiting stronger aggregate evidence.')}\n\n"
        f"**Affected sectors:** {sectors}.\n\n"
        f"**Detected from:** Search trends, public news, food price data, and official statistics. Current strongest source summary: {top.get('source_summary', 'Aggregate public sources')}.\n\n"
        + "\n\n".join(context_lines)
        + "\n\n"
        f"**Confidence reasoning:** {top.get('confidence_reasoning', 'Confidence reflects current aggregate evidence and will adapt as memory grows.')}\n\n"
        f"**Behavioral intelligence:** {_behavioral_interpretation(top)}\n\n"
        "Food affordability pressure is not treated as important because of one isolated mention. Its importance rises when related searches, public news, price signals, and county-level recurrence persist together over time.\n\n"
        "Scores improve over time through adaptive signal memory, source agreement, validation checks, historical pattern matching, semantic clustering, prediction feedback, and analyst feedback.\n\n"
        f"**Privacy note:** {PRIVACY_NOTE}"
    )


def render_historical_learning_insight(signals: list[dict[str, Any]]) -> str:
    top = (signals or [_friendly_empty_signal()])[0]
    return "### Historical Learning Insight\n\n" + _historical_learning_insight(top)


def _repeat_for_continuous_loop(signals: list[dict[str, Any]], minimum: int = 5) -> list[dict[str, Any]]:
    if not signals:
        return [_friendly_empty_signal() for _ in range(minimum)]
    repeated = list(signals)
    while len(repeated) < minimum:
        repeated.extend(signals)
    return repeated[: max(minimum, len(repeated))]


def _filter_signals(signals: list[dict[str, Any]], location: str, category: str, urgency: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for signal in signals:
        if category != "All" and str(signal.get("signal_category", "")).lower() != category.lower():
            continue
        if urgency != "All" and str(signal.get("urgency", "")).lower() != urgency.lower():
            continue
        if location not in {"", "All", "Kenya", "Global"}:
            scope = str(signal.get("geographic_scope", "")).lower()
            topic = str(signal.get("signal_topic", "")).lower()
            if location.lower() not in scope and location.lower() not in topic:
                continue
        output.append(signal)
    return output


def _friendly_empty_signal() -> dict[str, Any]:
    return {
        "signal_topic": "Kenya aggregate signal monitor active",
        "signal_category": "other",
        "demand_level": "Moderate",
        "opportunity_level": "Moderate",
        "unmet_demand_likelihood": "Medium",
        "urgency": "Medium",
        "geographic_scope": "Kenya-wide",
        "source_summary": "Sample aggregate signal",
        "confidence_score": 50,
        "last_updated": "recently",
        "recommended_action": "Keep monitoring aggregate public signals while live sources refresh.",
        "momentum": "Stable",
        "interpretation": "The feed is active and will update as aggregate public signals are available.",
        "privacy_level": "aggregate_public",
        "predicted_direction": "stable",
        "forecast_direction": "Stable",
        "forecast_confidence": 50,
        "spread_risk": "Low",
        "historical_pattern_match": "No close historical pattern yet",
        "historical_lesson_used": "Historical memory is still accumulating lessons for this signal type.",
        "likely_next_development": "The system will keep monitoring persistence, validation, and related signals.",
        "confidence_reasoning": "Confidence reflects current aggregate evidence and will adapt as memory grows.",
        "behavioral_families": ["Demand"],
        "behavioral_intelligence_score": 50,
        "persistence_score": 35,
        "cross_source_confirmation_score": 35,
        "geographic_spread_score": 45,
        "historical_recurrence_score": 10,
        "learning_note": "Collective behavioral evidence is still accumulating.",
        "adaptation_note": "Behavioral scoring remains conservative until signals persist.",
        "opportunity_interpretation": "Behavioral family evidence is developing.",
    }


def _card(signal: dict[str, Any]) -> str:
    topic = escape(str(signal.get("signal_topic", "Kenya signal")))
    category = escape(str(signal.get("signal_category", "other")))
    momentum = escape(MOMENTUM_BADGES.get(str(signal.get("momentum")), str(signal.get("momentum", "Stable"))))
    demand = escape(str(signal.get("demand_level", "Moderate")))
    opportunity = escape(str(signal.get("opportunity_level", "Moderate")))
    unmet = escape(str(signal.get("unmet_demand_likelihood", "Medium")))
    urgency = escape(str(signal.get("urgency", "Medium")))
    scope = escape(str(signal.get("geographic_scope", "Kenya-wide")))
    source = escape(str(signal.get("source_summary", "Aggregate public sources")))
    confidence = escape(str(signal.get("confidence_score", 0)))
    updated = escape(str(signal.get("last_updated", "")))
    action = escape(str(signal.get("recommended_action", "Monitor and validate with aggregate data.")))
    score_note = escape(str(signal.get("confidence_reasoning") or signal.get("score_explanation", "Adaptive score uses aggregate evidence and validation signals.")))
    badges = "".join(f"<span class='signal-card-category'>{escape(badge)}</span>" for badge in _badges(signal, category, momentum))
    forecast = escape(str(signal.get("forecast_direction") or signal.get("predicted_direction", "stable")))
    spread = escape(str(signal.get("spread_risk", "Low")))
    return (
        "<article class='signal-card'>"
        f"<div class='signal-card-topic'>{topic}</div>"
        f"<div>{badges}</div>"
        "<div class='signal-card-grid'>"
        f"<span><strong>Demand</strong>{demand}</span>"
        f"<span><strong>Opportunity</strong>{opportunity}</span>"
        f"<span><strong>Unmet need</strong>{unmet}</span>"
        f"<span><strong>Urgency</strong>{urgency}</span>"
        f"<span><strong>Scope</strong>{scope}</span>"
        f"<span><strong>Source</strong>{source}</span>"
        f"<span><strong>Forecast</strong>{forecast}</span>"
        f"<span><strong>Spread risk</strong>{spread}</span>"
        f"<span><strong>Confidence</strong>{confidence}%</span>"
        "</div>"
        f"<p>{action}</p>"
        f"<div class='signal-card-time' title='{score_note}'>Last updated: {updated}</div>"
        "</article>"
    )



def _behavioral_interpretation(signal: dict[str, Any]) -> str:
    families = signal.get("behavioral_families") or ["Demand"]
    family_text = ", ".join(str(family) for family in families)
    score = signal.get("behavioral_intelligence_score", 0)
    persistence = signal.get("persistence_score", 0)
    source = signal.get("cross_source_confirmation_score", 0)
    spread = signal.get("geographic_spread_score", 0)
    recurrence = signal.get("historical_recurrence_score", 0)
    note = signal.get("opportunity_interpretation") or signal.get("learning_note") or "Collective behavioral evidence is still developing."
    return (
        f"This is classified as {family_text}. Score {score}/100 reflects persistence {persistence}/100, "
        f"source confirmation {source}/100, geographic spread {spread}/100, and historical recurrence {recurrence}/100. {note}"
    )
def _historical_learning_insight(signal: dict[str, Any]) -> str:
    pattern = signal.get("historical_pattern_match", "No close historical pattern yet")
    direction = signal.get("forecast_direction") or str(signal.get("predicted_direction", "stable")).title()
    confidence = signal.get("forecast_confidence", signal.get("confidence_score", 0))
    next_step = signal.get("likely_next_development", "The system will keep monitoring persistence, validation, and related signals.")
    lesson = signal.get("historical_lesson_used", "Historical memory is still accumulating lessons for this signal type.")
    return (
        f"Today's signal pattern: **{pattern}**. "
        f"Historical memory suggests the next direction is **{direction}** with confidence **{confidence}%**. "
        f"{next_step} Historical lesson used: {lesson}"
    )


def _badges(signal: dict[str, Any], category: str, momentum: str) -> list[str]:
    badges = [category, momentum, _validation_badge(signal)]
    for family in signal.get("behavioral_families", [])[:4]:
        badges.append(_family_badge(str(family)))
    persistence = str(signal.get("persistence_badge") or ("Breakout" if signal.get("momentum") == "Breakout" else "Emerging"))
    badges.append(persistence)
    badges.append("County-specific" if str(signal.get("geographic_scope", "Kenya-wide")) != "Kenya-wide" else "Kenya-wide")
    if float(signal.get("multi_source_confirmation_score", 0) or 0) >= 65:
        badges.append("Multi-source")
    for label in signal.get("early_warning_labels", [])[:2]:
        badges.append(str(label))
    if signal.get("forecast_direction") == "Rising" or signal.get("predicted_direction") == "rising":
        badges.append("Forecast rising")
    if signal.get("spread_risk") in {"Moderate", "High"}:
        badges.append("County spread risk")
    if signal.get("historical_pattern_match") and signal.get("historical_pattern_match") != "No close historical pattern yet":
        badges.append("Historical match")
    if float(signal.get("behavioral_intelligence_score", 0) or 0) >= 65:
        badges.append("Collective signal")
    return _dedupe_badges(badges)[:8]


def _dedupe_badges(badges: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for badge in badges:
        if badge and badge not in seen:
            seen.add(badge)
            output.append(badge)
    return output


def _family_badge(family: str) -> str:
    return {
        "Demand": "Demand signal",
        "Affordability": "Affordability pressure",
        "Stress": "Stress signal",
        "Opportunity": "Opportunity signal",
    }.get(family, family)


def _validation_badge(signal: dict[str, Any]) -> str:
    status = str(signal.get("validation_status", "unvalidated"))
    if status == "validated":
        return "Validated"
    if status == "partially_validated":
        return "Partially validated"
    return "Emerging"
