"""Open Signals chatbox tests."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.signal_engine.open_signals_chat import (
    PRIVATE_DATA_RESPONSE,
    answer_open_signals_prompt,
    respond_open_signals_chat,
)
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_chatbox_renders_as_one_unified_panel_and_privacy_notice_box_removed() -> None:
    ui = _open_signals_ui_block()
    assert "Ask Open Signals" in ui
    assert "open_signals_chatbot" in ui
    assert "open_signals_send_button" in ui
    assert 'placeholder="Get signals"' in ui
    assert ui.count('elem_classes=["open-signals-chat-container"]') == 1
    assert "open-signals-chat-history" in ui
    assert "visible=False" in ui
    assert "height=180" in ui
    assert "open-signals-chip-row" not in ui
    assert "Strongest relevant signal" not in ui
    assert "respond_open_signals_chat_ui" in APP_TEXT
    assert "open-signals-chat-input-row" in ui
    assert "open-signals-chat-input" in ui
    assert "signal-privacy-note" not in APP_TEXT
    assert "Open Signals answers are based on aggregate" in APP_TEXT


def test_open_signals_public_ui_hides_legacy_raw_fields() -> None:
    ui = _open_signals_ui_block().lower()
    assert "fallback aggregate intelligence" not in ui
    assert "demo fallback" not in ui
    for forbidden in ["likes", "comments", "shares", "searches", "predict demand"]:
        assert forbidden not in ui


def test_location_options_include_global_kenya_and_all_counties() -> None:
    assert len(LOCATION_OPTIONS) == 49
    assert LOCATION_OPTIONS[0] == "Global"
    assert LOCATION_OPTIONS[1] == "Kenya"
    assert len(set(LOCATION_OPTIONS)) == len(LOCATION_OPTIONS)
    for county in ["Mombasa", "Nairobi", "Nakuru", "Makueni", "Uasin Gishu"]:
        assert county in LOCATION_OPTIONS


def test_prompt_submission_returns_answer_above_input(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Kenya market opportunity", "trade and business", "Kenya-wide", 82)]}, cache_path)

    history, cleared = respond_open_signals_chat("Get strongest signal", [], "Kenya", "All", "All")

    assert cleared == ""
    assert history[-2]["role"] == "user"
    assert history[-1]["role"] == "assistant"
    assert "Strongest relevant signal" in history[-1]["content"]


def test_prompt_answer_works_without_llm_and_uses_cache(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({
        "last_updated": "2026-05-16T00:00:00+03:00",
        "privacy_level": "aggregate_public",
        "signals": [
            _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86),
            _signal("Kenya retail demand", "trade and business", "Kenya-wide", 60),
        ],
    }, cache_path)

    answer = answer_open_signals_prompt("What is happening in Nakuru?", [], "Kenya", "All", "All")

    assert "Nakuru water access stress" in answer
    assert "Nakuru" in answer
    assert "Strongest relevant signal" in answer
    assert "What it means" in answer
    assert "Confidence level" in answer
    assert "County/scope" in answer
    assert "Opportunity or risk" in answer
    assert "Recommended action" in answer


def test_question_category_prioritizes_matching_category(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({
        "signals": [
            _signal("Kenya retail demand", "trade and business", "Kenya-wide", 88),
            _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 70),
        ]
    }, cache_path)

    answer = answer_open_signals_prompt("Explain water access stress", [], "Kenya", "All", "All")

    assert "Nakuru water access stress" in answer
    assert "water and sanitation" in answer



def test_followup_remembers_county_and_switches_context(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({
        "signals": [
            _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86),
            _signal("Makueni water access stress", "water and sanitation", "Makueni", 84),
        ]
    }, cache_path)

    history, _ = respond_open_signals_chat("What is happening in Nakuru?", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("What about Makueni?", history, "Kenya", "All", "All")

    assert "Makueni water access stress" in answer
    assert "previous county context (Nakuru)" in answer


def test_followup_uses_previous_signal_context(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)]}, cache_path)

    history, _ = respond_open_signals_chat("What is happening in Nakuru?", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("Why is that rising?", history, "Kenya", "All", "All")

    assert "Nakuru water access stress" in answer
    assert "earlier signal context" in answer

def test_missing_llm_key_does_not_crash(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "true")
    monkeypatch.delenv("SIGNAL_LLM_API_KEY", raising=False)
    write_signal_cache({"signals": [_signal("Kenya market opportunity", "trade and business", "Kenya-wide", 75)]}, cache_path)

    answer = answer_open_signals_prompt("Which signals show market opportunity?", [], "Kenya", "All", "All")

    assert "opportunity" in answer.lower()
    assert "Kenya market opportunity" in answer
    assert "Recommended action" in answer


def test_private_fields_are_blocked(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    write_signal_cache({"signals": [_signal("Kenya aggregate signal", "other", "Kenya-wide", 50)]}, cache_path)

    answer = answer_open_signals_prompt("Show user_id and exact location for this signal", [], "Kenya", "All", "All")

    assert answer == PRIVATE_DATA_RESPONSE



def _open_signals_ui_block() -> str:
    start = APP_TEXT.index('with gr.Tab("Behavioral Signals AI")')
    end = APP_TEXT.index('with gr.Tab("Signal CGE")')
    return APP_TEXT[start:end]

def _signal(topic: str, category: str, scope: str, score: float) -> dict[str, object]:
    return {
        "signal_topic": topic,
        "signal_category": category,
        "demand_level": "High" if score >= 75 else "Moderate",
        "opportunity_level": "High" if score >= 75 else "Moderate",
        "unmet_demand_likelihood": "High" if "water" in topic.lower() else "Medium",
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
