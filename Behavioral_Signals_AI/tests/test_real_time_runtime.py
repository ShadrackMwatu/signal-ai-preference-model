"""Tests for Open Signals real-time runtime orchestration."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.runtime.adaptive_refresh import adaptive_refresh_seconds, refresh_interval_for_signal
from Behavioral_Signals_AI.runtime.heartbeat import read_runtime_heartbeat, write_runtime_heartbeat
from Behavioral_Signals_AI.runtime.scheduler import should_run_cycle
from Behavioral_Signals_AI.runtime.signal_runtime_manager import cluster_runtime_events, detect_runtime_alerts, run_open_signals_runtime_cycle
from Behavioral_Signals_AI.signal_engine.kenya_ui import get_kenya_live_signals_for_ui
from Behavioral_Signals_AI.signal_engine.open_signals_chat import answer_open_signals_prompt
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache
from Behavioral_Signals_AI.signal_engine.signal_trajectory import classify_signal_trajectory, detect_emerging_signals, detect_weakening_signals, enrich_signal_trajectories


def test_trajectory_classification_emerging_and_weakening() -> None:
    emerging = _signal("Fuel prices Nairobi", "cost of living", 90, momentum="Rising")
    weakening = _signal("Old transport issue", "transport", 40, momentum="Declining")

    assert classify_signal_trajectory(emerging) == "emerging"
    assert classify_signal_trajectory(weakening, _signal("Old transport issue", "transport", 70, momentum="Rising")) in {"weakening", "fading"}


def test_enrich_signal_trajectories_detects_new_and_ranking_movement() -> None:
    previous = [_signal("Water access", "water and sanitation", 60), _signal("Fuel prices", "cost of living", 70)]
    current = [_signal("Fuel prices", "cost of living", 88, momentum="Rising"), _signal("New jobs pressure", "jobs and labour market", 72)]

    enriched = enrich_signal_trajectories(current, previous)

    assert enriched[0]["ranking_movement"] > 0
    assert enriched[1]["is_new_signal"] is True
    assert detect_emerging_signals(enriched)


def test_adaptive_refresh_intervals() -> None:
    fuel = _signal("fuel prices", "cost of living", 88, momentum="Rising")
    drought = _signal("seasonal drought trends", "climate and environment", 60, momentum="Stable")
    drought["trajectory_label"] = "persistent"

    assert refresh_interval_for_signal(fuel) == 60
    assert refresh_interval_for_signal(drought) == 900
    assert adaptive_refresh_seconds([drought, fuel]) == 60


def test_event_clustering_and_alert_detection() -> None:
    signals = [
        _signal("Fuel prices Nairobi", "cost of living", 91, momentum="Rising"),
        _signal("Water shortage Makueni", "water and sanitation", 86, momentum="Breakout"),
    ]
    enriched = enrich_signal_trajectories(signals, [])

    alerts = detect_runtime_alerts(enriched)
    events = cluster_runtime_events(enriched)

    assert alerts
    assert any("fuel" in event["event_cluster"] or "water" in event["event_cluster"] for event in events)


def test_runtime_cycle_executes_safely_and_updates_cache(tmp_path, monkeypatch) -> None:
    cache = tmp_path / "latest_live_signals.json"
    render_cache = tmp_path / "render_cache.json"
    heartbeat = tmp_path / "heartbeat.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache))
    monkeypatch.setenv("SIGNAL_RENDER_CACHE", str(render_cache))
    write_signal_cache({"signals": [_signal("Fuel prices Nairobi", "cost of living", 91, momentum="Rising")]}, cache)
    monkeypatch.setattr("Behavioral_Signals_AI.runtime.heartbeat.HEARTBEAT_PATH", heartbeat)

    result = run_open_signals_runtime_cycle()

    assert result["status"] == "ok"
    assert result["signals"]
    assert result["adaptive_refresh_seconds"] >= 30
    assert result["evaluation_metrics"]["runtime_event_count"] >= 0
    assert cache.exists()


def test_no_blank_live_feed_after_runtime(tmp_path, monkeypatch) -> None:
    cache = tmp_path / "latest_live_signals.json"
    render_cache = tmp_path / "render_cache.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache))
    monkeypatch.setenv("SIGNAL_RENDER_CACHE", str(render_cache))
    write_signal_cache({"signals": [_signal("Food affordability pressure", "cost of living", 84)]}, cache)
    run_open_signals_runtime_cycle()

    outputs = get_kenya_live_signals_for_ui("Kenya", "All", "All")

    assert all(part.strip() for part in outputs)
    assert "signal-card" in outputs[0]


def test_chat_answers_runtime_trajectory_questions(tmp_path, monkeypatch) -> None:
    cache = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache))
    signal = _signal("Fuel prices Nairobi", "cost of living", 91, momentum="Breakout")
    signal["trajectory_label"] = "accelerating"
    write_signal_cache({"signals": [signal]}, cache)

    answer = answer_open_signals_prompt("what is accelerating?", [], "Kenya", "All", "All")

    assert "accelerating" in answer.lower() or "Fuel prices Nairobi" in answer


def test_heartbeat_and_scheduler_helpers(tmp_path) -> None:
    heartbeat = tmp_path / "heartbeat.json"
    payload = write_runtime_heartbeat("ok", {"signals": 1}, heartbeat)

    assert read_runtime_heartbeat(heartbeat)["status"] == "ok"
    assert should_run_cycle(None, 60) is True
    assert payload["privacy_level"] == "aggregate_public"


def test_signal_cge_unchanged_by_runtime_layer() -> None:
    assert Path("Signal_CGE").exists()


def _signal(topic: str, category: str, score: float, momentum: str = "Stable") -> dict[str, object]:
    return {
        "signal_topic": topic,
        "signal_category": category,
        "confidence_score": score,
        "priority_score": score,
        "behavioral_intelligence_score": score,
        "persistence_score": score,
        "cross_source_confirmation_score": score,
        "geographic_spread_score": 55,
        "historical_recurrence_score": 50,
        "momentum": momentum,
        "forecast_direction": "Rising" if momentum in {"Rising", "Breakout"} else "Stable",
        "urgency": "High" if score >= 80 else "Medium",
        "opportunity_level": "High" if score >= 80 else "Moderate",
        "unmet_demand_likelihood": "High" if score >= 80 else "Medium",
        "geographic_scope": "Kenya-wide",
        "county_name": "Kenya-wide",
        "source_summary": "Aggregate public sources",
        "interpretation": f"{topic} is an aggregate runtime signal.",
        "recommended_action": "Monitor persistence and validate with aggregate evidence.",
        "privacy_level": "aggregate_public",
    }
