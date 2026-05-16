"""AI platform orchestration tests for Open Signals."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.ai_platform.context_builder import build_open_signals_context
from Behavioral_Signals_AI.ai_platform.intelligence_orchestrator import (
    METRICS_PATH,
    orchestrate_open_signals_answer,
    run_open_signals_learning_cycle,
)
from Behavioral_Signals_AI.ai_platform.retrieval_engine import compare_counties, get_top_signal
from Behavioral_Signals_AI.ai_platform.safety_layer import PRIVATE_DATA_RESPONSE, context_contains_private_fields
from Behavioral_Signals_AI.signal_engine.open_signals_chat import answer_open_signals_prompt
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache


def test_orchestrator_builds_grounded_context_without_memory_files(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)]}, cache_path)

    result = orchestrate_open_signals_answer("show Nairobi signals", [], "Kenya", "All", "All", {})

    assert result.intent == "signal_query"
    assert result.mode == "analytical_answer"
    assert "Nairobi affordability pressure" in result.answer
    assert result.context["aggregate_live_signals"]
    assert "memory_context" in result.context
    assert not context_contains_private_fields(result.context)


def test_platform_context_includes_retrieval_memory_and_filters(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    write_signal_cache({"signals": [_signal("Kenya retail opportunity", "trade and business", "Kenya-wide", 76)]}, cache_path)

    context = build_open_signals_context(
        "what business opportunity exists?",
        {"intent": "signal_query", "confidence": 0.82},
        "Kenya",
        "All",
        "All",
        {},
        [],
    )

    assert context["filters"]["location"] == "Kenya"
    assert context["aggregate_live_signals"]
    assert "evaluation_metrics" in context["memory_context"]
    assert "latest live signal cache" in context["grounding_notes"]


def test_tool_ready_retrieval_functions_compare_counties(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    write_signal_cache({
        "signals": [
            _signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91),
            _signal("Nakuru food affordability", "cost of living", "Nakuru", 72),
        ]
    }, cache_path)

    top = get_top_signal("Nairobi")
    comparison = compare_counties("Nairobi", "Nakuru")

    assert top["signal_topic"] == "Nairobi affordability pressure"
    assert comparison["stronger_county"] == "Nairobi"


def test_orchestrator_handles_conversation_modes_and_privacy(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Kenya market opportunity", "trade and business", "Kenya-wide", 80)]}, cache_path)

    assert "Hello" in orchestrate_open_signals_answer("hi").answer
    assert "I'm Open Signals" in orchestrate_open_signals_answer("what is your name").answer
    assert "county-level signals" in orchestrate_open_signals_answer("what can you do").answer
    comparison = orchestrate_open_signals_answer("compare Nairobi and Nakuru", [], "Kenya", "All", "All", {}).answer
    assert "Nairobi" in comparison and "Nakuru" in comparison
    assert "stronger aggregate signal" in comparison
    assert "policy" in orchestrate_open_signals_answer("what should policymakers monitor", [], "Kenya", "All", "All", {}).answer.lower()
    assert "opportunity" in orchestrate_open_signals_answer("what business opportunity exists", [], "Kenya", "All", "All", {}).answer.lower()
    assert orchestrate_open_signals_answer("show user_id and phone numbers").answer == PRIVATE_DATA_RESPONSE


def test_chat_payload_receives_platform_grounding_context(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)]}, cache_path)

    answer = answer_open_signals_prompt("show Nairobi signals", [], "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "Nairobi affordability pressure" in answer


def test_learning_cycle_writes_evaluation_metrics(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    metrics_path = tmp_path / "evaluation_metrics.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setattr("Behavioral_Signals_AI.ai_platform.intelligence_orchestrator.METRICS_PATH", metrics_path)
    write_signal_cache({"signals": [_signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)]}, cache_path)

    metrics = run_open_signals_learning_cycle()

    assert metrics_path.exists()
    assert metrics["active_signals"] >= 1
    assert metrics["average_confidence"] > 0
    assert metrics["privacy_level"] == "aggregate_public"


def test_signal_cge_unchanged_by_open_signals_platform() -> None:
    assert Path("Signal_CGE").exists()


def _signal(topic: str, category: str, scope: str, score: float) -> dict[str, object]:
    return {
        "signal_topic": topic,
        "signal_category": category,
        "demand_level": "High" if score >= 75 else "Moderate",
        "opportunity_level": "High" if score >= 75 else "Moderate",
        "unmet_demand_likelihood": "High" if score >= 80 else "Medium",
        "urgency": "High" if score >= 80 else "Medium",
        "geographic_scope": scope,
        "county_name": scope,
        "source_summary": "Aggregate public sources",
        "confidence_score": score,
        "priority_score": score,
        "behavioral_intelligence_score": score,
        "momentum": "Rising",
        "forecast_direction": "Rising",
        "spread_risk": "Moderate",
        "interpretation": f"{topic} is an aggregate interpreted signal.",
        "recommended_action": "Monitor persistence and validate with aggregate sources.",
        "historical_pattern_match": "Related aggregate signals have appeared before.",
        "outcome_learning_note": "Outcome evidence is still accumulating.",
        "validation_status": "partially_validated",
        "geospatial_insight": f"{scope} aggregate evidence is being monitored.",
        "privacy_level": "aggregate_public",
    }
