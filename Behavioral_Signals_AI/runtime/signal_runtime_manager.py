"""Real-time intelligence orchestration for Open Signals."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.ai_platform.intelligence_orchestrator import build_evaluation_metrics
from Behavioral_Signals_AI.runtime.adaptive_refresh import adaptive_refresh_seconds
from Behavioral_Signals_AI.runtime.heartbeat import write_runtime_heartbeat
from Behavioral_Signals_AI.signal_engine.open_signals_learning_cycle import run_open_signals_learning_cycle
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals, write_signal_cache
from Behavioral_Signals_AI.signal_engine.signal_trajectory import detect_emerging_signals, detect_weakening_signals, enrich_signal_trajectories
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display, save_rendered_outputs, signal_signature

RUNTIME_STATE_PATH = Path("Behavioral_Signals_AI/outputs/runtime_signal_state.json")
ALERTS_PATH = Path("Behavioral_Signals_AI/outputs/runtime_signal_alerts.json")
EVENTS_PATH = Path("Behavioral_Signals_AI/outputs/runtime_signal_events.json")


def run_open_signals_runtime_cycle() -> dict[str, Any]:
    """Run one autonomous aggregate-intelligence refresh cycle."""
    previous_payload = get_cached_or_fallback_signals()
    previous_signals = [signal for signal in previous_payload.get("signals", []) if isinstance(signal, dict)]
    learning_result = run_open_signals_learning_cycle()
    current_payload = get_cached_or_fallback_signals()
    current_signals = [signal for signal in current_payload.get("signals", []) if isinstance(signal, dict)]
    enriched = enrich_signal_trajectories(current_signals, previous_signals)
    ranked = rank_signals_for_display(_decay_fading_signals(enriched))
    if not ranked:
        ranked = previous_signals or [_friendly_runtime_signal()]
    write_signal_cache({
        "last_updated": datetime.now(UTC).isoformat(),
        "status": "runtime_cycle_updated",
        "signals": ranked,
        "privacy_level": "aggregate_public",
    })
    alerts = detect_runtime_alerts(ranked)
    events = cluster_runtime_events(ranked)
    refresh_seconds = adaptive_refresh_seconds(ranked)
    metrics = _runtime_metrics(ranked, alerts, events, refresh_seconds)
    _write_runtime_outputs(alerts, events, metrics)
    _update_render_cache(ranked)
    heartbeat = write_runtime_heartbeat("ok", {"signals": len(ranked), "alerts": len(alerts), "events": len(events), "refresh_seconds": refresh_seconds})
    return {
        "status": "ok",
        "signals": ranked,
        "emerging_signals": detect_emerging_signals(ranked),
        "weakening_signals": detect_weakening_signals(ranked),
        "alerts": alerts,
        "events": events,
        "adaptive_refresh_seconds": refresh_seconds,
        "evaluation_metrics": metrics,
        "learning_result": learning_result,
        "heartbeat": heartbeat,
        "multimodal_stubs": _multimodal_stubs(),
        "privacy_level": "aggregate_public",
    }


def detect_runtime_alerts(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    alerts = []
    for signal in signals:
        score = _score(signal)
        trajectory = str(signal.get("trajectory_label", ""))
        spread = str(signal.get("spread_risk", ""))
        category = str(signal.get("signal_category", ""))
        if trajectory == "accelerating" or score >= 88:
            alerts.append(_alert(signal, "rapid_signal_spike", "Rapid aggregate signal spike detected"))
        if spread.lower() == "high" or _num(signal.get("geographic_spread_score")) >= 75:
            alerts.append(_alert(signal, "unusual_county_spread", "Unusual county spread detected"))
        if category in {"cost of living", "food and agriculture"} and str(signal.get("urgency", "")).lower() == "high":
            alerts.append(_alert(signal, "affordability_stress", "Sudden affordability stress pattern detected"))
        if str(signal.get("opportunity_level", "")).lower() == "high" and score >= 75:
            alerts.append(_alert(signal, "market_opportunity", "Emerging market opportunity detected"))
        if trajectory == "persistent" and _num(signal.get("confidence_score")) >= 75:
            alerts.append(_alert(signal, "persistent_high_confidence", "High-confidence persistent signal detected"))
    return _dedupe_alerts(alerts)


def cluster_runtime_events(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for signal in signals:
        clusters[_event_key(signal)].append(signal)
    events = []
    for key, items in clusters.items():
        if not items:
            continue
        top = rank_signals_for_display(items)[0]
        counties = sorted({str(item.get("county_name") or item.get("geographic_scope") or "Kenya-wide") for item in items})
        sources = sorted({str(item.get("source_summary") or "Aggregate sources")[:80] for item in items})
        events.append({
            "event_cluster": key,
            "top_signal": top.get("signal_topic"),
            "category": top.get("signal_category"),
            "signal_count": len(items),
            "county_scope": counties[:8],
            "source_agreement": len(sources),
            "trajectory": top.get("trajectory_label"),
            "confidence": top.get("confidence_score"),
            "privacy_level": "aggregate",
        })
    return sorted(events, key=lambda event: (event["signal_count"], event.get("confidence") or 0), reverse=True)[:12]


def _decay_fading_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for signal in signals:
        item = dict(signal)
        if item.get("trajectory_label") == "fading":
            item["priority_score"] = max(0, _num(item.get("priority_score")) - 8)
            item["confidence_score"] = max(0, _num(item.get("confidence_score")) - 4)
        if _score(item) >= 25:
            output.append(item)
    return output


def _write_runtime_outputs(alerts: list[dict[str, Any]], events: list[dict[str, Any]], metrics: dict[str, Any]) -> None:
    payload_base = {"generated_at": datetime.now(UTC).isoformat(), "privacy_level": "aggregate_public"}
    write_json(ALERTS_PATH, {**payload_base, "alerts": alerts})
    write_json(EVENTS_PATH, {**payload_base, "events": events})
    write_json(RUNTIME_STATE_PATH, {**payload_base, "metrics": metrics})
    existing = read_json("Behavioral_Signals_AI/outputs/evaluation_metrics.json", {})
    if not isinstance(existing, dict):
        existing = {}
    existing.update(metrics)
    write_json("Behavioral_Signals_AI/outputs/evaluation_metrics.json", existing)


def _update_render_cache(signals: list[dict[str, Any]]) -> None:
    try:
        from Behavioral_Signals_AI.signal_engine.kenya_ui import render_emerging_signals, render_historical_learning_insight, render_live_signal_feed, render_strategic_interpretation

        outputs = (
            render_live_signal_feed(signals, datetime.now(UTC).isoformat()),
            render_emerging_signals(signals),
            render_strategic_interpretation(signals),
            render_historical_learning_insight(signals),
        )
        if all(part.strip() for part in outputs):
            save_rendered_outputs("kenya|all|all", signal_signature(signals), outputs)
    except Exception:
        pass


def _runtime_metrics(signals: list[dict[str, Any]], alerts: list[dict[str, Any]], events: list[dict[str, Any]], refresh_seconds: int) -> dict[str, Any]:
    base = build_evaluation_metrics(signals, {})
    source_freshness = _source_freshness(signals)
    base.update({
        "trajectory_accuracy": None,
        "emerging_signal_confirmation_rate": None,
        "false_spike_rate": None,
        "county_spread_prediction_accuracy": None,
        "runtime_source_uptime": 1.0 if signals else 0.0,
        "source_freshness": source_freshness,
        "runtime_alert_count": len(alerts),
        "runtime_event_count": len(events),
        "adaptive_refresh_seconds": refresh_seconds,
        "emerging_signal_count": len(detect_emerging_signals(signals)),
        "weakening_signal_count": len(detect_weakening_signals(signals)),
    })
    return base


def _source_freshness(signals: list[dict[str, Any]]) -> dict[str, Any]:
    return {"last_updated": datetime.now(UTC).isoformat(), "active_signal_count": len(signals)}


def _alert(signal: dict[str, Any], alert_type: str, note: str) -> dict[str, Any]:
    return {
        "alert_type": alert_type,
        "signal_topic": signal.get("signal_topic"),
        "category": signal.get("signal_category"),
        "county_or_scope": signal.get("county_name") or signal.get("geographic_scope"),
        "trajectory": signal.get("trajectory_label"),
        "confidence": signal.get("confidence_score"),
        "note": note,
        "privacy_level": "aggregate",
    }


def _dedupe_alerts(alerts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    output = []
    for alert in alerts:
        key = (alert.get("alert_type"), alert.get("signal_topic"), alert.get("county_or_scope"))
        if key not in seen:
            seen.add(key)
            output.append(alert)
    return output[:20]


def _event_key(signal: dict[str, Any]) -> str:
    topic = str(signal.get("signal_topic", "")).lower()
    category = str(signal.get("signal_category") or "other")
    if "fuel" in topic:
        return "fuel price pressure event"
    if "drought" in topic or "water" in topic:
        return "drought or water stress cluster"
    if "transport" in topic or "matatu" in topic:
        return "transport disruption cluster"
    if "hospital" in topic or "health" in topic:
        return "healthcare stress cluster"
    if "food" in topic or "maize" in topic or "unga" in topic:
        return "food affordability pressure event"
    return f"{category} signal cluster"


def _multimodal_stubs() -> dict[str, str]:
    return {
        "image_trend_understanding": "placeholder_only_not_active",
        "map_overlays": "placeholder_only_not_active",
        "chart_generation": "placeholder_only_not_active",
        "document_ingestion": "placeholder_only_not_active",
        "speech_audio_trend_ingestion": "placeholder_only_not_active",
    }


def _friendly_runtime_signal() -> dict[str, Any]:
    return {
        "signal_topic": "Open Signals runtime monitor active",
        "signal_category": "other",
        "confidence_score": 50,
        "priority_score": 50,
        "urgency": "Medium",
        "momentum": "Stable",
        "trajectory_label": "stabilizing",
        "geographic_scope": "Kenya-wide",
        "source_summary": "Aggregate runtime monitor",
        "privacy_level": "aggregate_public",
    }


def _score(signal: dict[str, Any]) -> float:
    return max(_num(signal.get("priority_score")), _num(signal.get("behavioral_intelligence_score")), _num(signal.get("confidence_score")))


def _num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
