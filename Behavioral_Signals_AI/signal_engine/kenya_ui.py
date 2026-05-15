"""UI renderer for Kenya live aggregate signals."""

from __future__ import annotations

from html import escape
from typing import Any

from Behavioral_Signals_AI.privacy import PRIVACY_NOTE
from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals

MOMENTUM_BADGES = {
    "Rising": "Rising",
    "Stable": "Stable",
    "Declining": "Declining",
    "Breakout": "Breakout",
}


def get_kenya_live_signals_for_ui(location_filter: str = "Kenya", category_filter: str = "All", urgency_filter: str = "All") -> tuple[str, str, str]:
    signals = fuse_kenya_signals(location_filter or "Kenya", category_filter or "All", urgency_filter or "All")
    return render_live_signal_feed(signals), render_emerging_signals(signals), render_strategic_interpretation(signals)


def render_live_signal_feed(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return "<div class='signal-feed-container'><div class='signal-card'>No Kenya aggregate signal passed the current filters.</div></div>"
    cards = "".join(_card(signal) for signal in signals)
    return f"<div class='signal-feed-container'><div class='signal-feed-inner'>{cards}{cards}</div></div>"


def render_emerging_signals(signals: list[dict[str, Any]]) -> str:
    selected = [signal for signal in signals if signal.get("momentum") in {"Rising", "Breakout"} or signal.get("urgency") == "High"][:4]
    if not selected:
        selected = signals[:3]
    items = "".join(
        f"<li><strong>{escape(str(signal.get('signal_topic')))}</strong>: {escape(str(signal.get('momentum')))} momentum, {escape(str(signal.get('urgency')))} urgency, detected from {escape(str(signal.get('source_summary')))}.</li>"
        for signal in selected
    )
    return "<div class='signal-emerging'><h3>Emerging Kenya Signals</h3><ul>" + items + "</ul></div>"


def render_strategic_interpretation(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return f"### Signal Interpretation & Opportunity\n\nNo current Kenya-wide signal is available under the selected filters.\n\nDetected from: Search trends, public news, food price data, and official statistics.\n\n**Privacy note:** {PRIVACY_NOTE}"
    top = signals[0]
    sectors = ", ".join(sorted({str(signal.get("signal_category", "other")) for signal in signals[:5]}))
    return (
        "### Signal Interpretation & Opportunity\n\n"
        f"**Top signal:** {top['signal_topic']} ({top['signal_category']}). {top.get('interpretation', '')}\n\n"
        f"**Affected sectors:** {sectors}.\n\n"
        f"**Detected from:** Search trends, public news, food price data, and official statistics. Current strongest source summary: {top.get('source_summary', 'Aggregate public sources')}.\n\n"
        f"**Recommended near-term action:** {top.get('recommended_action', 'Monitor this signal and validate with additional aggregate data.')}\n\n"
        f"**Privacy note:** {PRIVACY_NOTE}"
    )


def _card(signal: dict[str, Any]) -> str:
    topic = escape(str(signal.get("signal_topic", "Kenya signal")))
    category = escape(str(signal.get("signal_category", "other")))
    momentum = escape(MOMENTUM_BADGES.get(str(signal.get("momentum")), str(signal.get("momentum", "Stable"))))
    demand = escape(str(signal.get("demand_level", "Moderate")))
    opportunity = escape(str(signal.get("opportunity_level", "Moderate")))
    urgency = escape(str(signal.get("urgency", "Medium")))
    scope = escape(str(signal.get("geographic_scope", "Kenya-wide")))
    source = escape(str(signal.get("source_summary", "Aggregate public sources")))
    confidence = escape(str(signal.get("confidence_score", 0)))
    updated = escape(str(signal.get("last_updated", "")))
    action = escape(str(signal.get("recommended_action", "Monitor and validate with aggregate data.")))
    return (
        "<article class='signal-card'>"
        f"<div class='signal-card-topic'>{topic}</div>"
        f"<div><span class='signal-card-category'>{category}</span><span class='signal-card-category'>{momentum}</span></div>"
        "<div class='signal-card-grid'>"
        f"<span><strong>Demand</strong>{demand}</span>"
        f"<span><strong>Opportunity</strong>{opportunity}</span>"
        f"<span><strong>Urgency</strong>{urgency}</span>"
        f"<span><strong>Scope</strong>{scope}</span>"
        f"<span><strong>Source</strong>{source}</span>"
        f"<span><strong>Confidence</strong>{confidence}%</span>"
        "</div>"
        f"<p>{action}</p>"
        f"<div class='signal-card-time'>Last updated: {updated}</div>"
        "</article>"
    )