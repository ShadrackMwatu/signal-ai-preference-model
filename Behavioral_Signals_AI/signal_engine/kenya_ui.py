"""UI renderer for Kenya live aggregate signals."""

from __future__ import annotations

from html import escape
from typing import Any

from Behavioral_Signals_AI.privacy import PRIVACY_NOTE
from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals

MOMENTUM_BADGES = {
    "Rising": "Rising",
    "Stable": "Stable",
    "Declining": "Declining",
    "Breakout": "Breakout",
}


def get_kenya_live_signals_for_ui(location_filter: str = "Kenya", category_filter: str = "All", urgency_filter: str = "All") -> tuple[str, str, str]:
    payload = get_cached_or_fallback_signals()
    signals = _filter_signals(list(payload.get("signals", [])), location_filter or "Kenya", category_filter or "All", urgency_filter or "All")
    if not signals:
        signals = list(payload.get("signals", []))
    if not signals:
        signals = fuse_kenya_signals(location_filter or "Kenya", category_filter or "All", urgency_filter or "All")
    if not signals:
        signals = [_friendly_empty_signal()]
    last_updated = str(payload.get("last_updated") or signals[0].get("last_updated") or "recently")
    return render_live_signal_feed(signals, last_updated), render_emerging_signals(signals), render_strategic_interpretation(signals)


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
    selected = [signal for signal in safe_signals if signal.get("momentum") in {"Rising", "Breakout"} or signal.get("urgency") == "High"][:4]
    if not selected:
        selected = safe_signals[:3]
    items = "".join(
        f"<li><strong>{escape(str(signal.get('signal_topic')))}</strong>: {escape(str(signal.get('momentum', 'Stable')))} momentum, {escape(str(signal.get('urgency', 'Medium')))} urgency, detected from {escape(str(signal.get('source_summary', 'Aggregate public sources')))}.</li>"
        for signal in selected
    )
    if not items:
        items = "<li>Kenya aggregate signal monitoring is active.</li>"
    return "<div class='signal-emerging'><h3>Emerging Kenya Signals</h3><ul>" + items + "</ul></div>"


def render_strategic_interpretation(signals: list[dict[str, Any]]) -> str:
    safe_signals = signals or [_friendly_empty_signal()]
    top = safe_signals[0]
    sectors = ", ".join(sorted({str(signal.get("signal_category", "other")) for signal in safe_signals[:5]})) or "Kenya aggregate demand"
    return (
        "### Signal Interpretation & Opportunity\n\n"
        f"**Top signal:** {top.get('signal_topic', 'Kenya aggregate signal')} ({top.get('signal_category', 'other')}). {top.get('interpretation', 'Signal monitoring is active and awaiting stronger aggregate evidence.')}\n\n"
        f"**Affected sectors:** {sectors}.\n\n"
        f"**Detected from:** Search trends, public news, food price data, and official statistics. Current strongest source summary: {top.get('source_summary', 'Aggregate public sources')}.\n\n"
        f"**Recommended near-term action:** {top.get('recommended_action', 'Monitor this signal and validate with additional aggregate data.')}\n\n"
        "Scores improve over time through adaptive signal memory, source agreement, validation checks, and analyst feedback.\n\n"
        f"**Privacy note:** {PRIVACY_NOTE}"
    )

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
    validation = escape(_validation_badge(signal))
    persistence = escape(str(signal.get("persistence_badge") or ("Breakout" if signal.get("momentum") == "Breakout" else "Emerging")))
    scope_badge = escape("County-specific" if str(signal.get("geographic_scope", "Kenya-wide")) != "Kenya-wide" else "Kenya-wide")
    score_note = escape(str(signal.get("score_explanation", "Adaptive score uses aggregate evidence and validation signals.")))
    return (
        "<article class='signal-card'>"
        f"<div class='signal-card-topic'>{topic}</div>"
        f"<div><span class='signal-card-category'>{category}</span><span class='signal-card-category'>{momentum}</span><span class='signal-card-category'>{validation}</span><span class='signal-card-category'>{persistence}</span><span class='signal-card-category'>{scope_badge}</span></div>"
        "<div class='signal-card-grid'>"
        f"<span><strong>Demand</strong>{demand}</span>"
        f"<span><strong>Opportunity</strong>{opportunity}</span>"
        f"<span><strong>Unmet need</strong>{unmet}</span>"
        f"<span><strong>Urgency</strong>{urgency}</span>"
        f"<span><strong>Scope</strong>{scope}</span>"
        f"<span><strong>Source</strong>{source}</span>"
        f"<span><strong>Confidence</strong>{confidence}%</span>"
        "</div>"
        f"<p>{action}</p>"
        f"<div class='signal-card-time' title='{score_note}'>Last updated: {updated}</div>"
        "</article>"
    )

def _validation_badge(signal: dict[str, Any]) -> str:
    status = str(signal.get("validation_status", "unvalidated"))
    if status == "validated":
        return "Validated"
    if status == "partially_validated":
        return "Partially validated"
    return "Emerging"