"""Open Signals chatbox tests."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.llm.safety_guardrails import contains_private_fields
from Behavioral_Signals_AI.signal_engine.open_signals_chat import (
    PRIVATE_DATA_RESPONSE,
    answer_open_signals_prompt,
    build_open_signals_llm_payload,
    respond_open_signals_chat,
)
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_chatbox_renders_as_custom_prompt_ui_without_blank_panel() -> None:
    ui = _open_signals_ui_block()
    assert "Ask Open Signals" in ui
    assert "open_signals_chat_state" in ui
    assert "open_signals_messages" in ui
    assert "open_signals_send_button" in ui
    assert 'placeholder="Get signals"' in ui
    assert 'gr.Chatbot' not in ui
    assert "open_signals_chatbot" not in ui
    assert "open-signals-chat-container" not in ui
    assert "open-signals-chat-history" not in ui
    assert "open-signals-chat-shell" in ui
    assert "open-signals-messages" in ui
    assert "open-signals-input-row" in ui
    assert "open-signals-input" in ui
    assert "open-signals-chip-row" not in ui
    assert "Strongest relevant signal" not in ui
    assert "submit_open_signals_prompt" in APP_TEXT
    assert "signal-privacy-note" not in APP_TEXT
    assert "Open Signals answers are based on aggregate" in APP_TEXT


def test_empty_history_renders_no_blank_chat_panel() -> None:
    from app import render_open_signals_messages

    assert render_open_signals_messages([]) == ""
    assert render_open_signals_messages(None) == ""


def test_prompt_submission_renders_user_and_assistant_messages(tmp_path, monkeypatch) -> None:
    from app import submit_open_signals_prompt

    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Kenya market opportunity", "trade and business", "Kenya-wide", 82)]}, cache_path)

    html, history, cleared = submit_open_signals_prompt("Get strongest signal", [], "Kenya", "All", "All")

    assert cleared == ""
    assert len(history) == 2
    assert "open-signals-user-msg" in html
    assert "open-signals-assistant-msg" in html
    assert "Get strongest signal" in html
    assert "Strongest relevant signal" in html

def test_open_signals_public_ui_hides_legacy_raw_fields() -> None:
    ui = _open_signals_ui_block().lower()
    assert "fallback aggregate intelligence" not in ui
    assert "demo fallback" not in ui
    for forbidden in ["likes", "comments", "shares", "searches", "predict demand"]:
        assert forbidden not in ui



def test_conversational_intent_detection_handles_greetings_and_help() -> None:
    assert detect_open_signals_intent("hi")["intent"] == "greeting"
    assert detect_open_signals_intent("hello")["intent"] == "greeting"
    assert detect_open_signals_intent("how are you?")["intent"] == "small_talk"
    assert detect_open_signals_intent("what can you do?")["intent"] == "capability_query"
    assert detect_open_signals_intent("what is your name?")["intent"] == "identity_query"
    assert detect_open_signals_intent("who are you?")["intent"] == "identity_query"
    assert detect_open_signals_intent("are you AI?")["intent"] == "identity_query"
    assert detect_open_signals_intent("what do you do?")["intent"] == "capability_query"
    assert detect_open_signals_intent("can you help me?")["intent"] == "capability_query"
    assert detect_open_signals_intent("what are signals?")["intent"] == "capability_query"
    assert detect_open_signals_intent("explain signals")["intent"] == "capability_query"
    assert detect_open_signals_intent("show signals in Nairobi")["intent"] == "signal_query"
    assert detect_open_signals_intent("compare Nakuru and Makueni")["intent"] == "comparison_query"


def test_greeting_and_small_talk_do_not_trigger_signal_analysis() -> None:
    hi = answer_open_signals_prompt("hi", [], "Kenya", "All", "All")
    hello = answer_open_signals_prompt("hello", [], "Kenya", "All", "All")
    how = answer_open_signals_prompt("how are you?", [], "Kenya", "All", "All")
    capabilities = answer_open_signals_prompt("what can you do?", [], "Kenya", "All", "All")
    identity = answer_open_signals_prompt("what is your name?", [], "Kenya", "All", "All")
    ai = answer_open_signals_prompt("are you AI?", [], "Kenya", "All", "All")
    explain = answer_open_signals_prompt("explain signals", [], "Kenya", "All", "All")

    assert any(word in hi for word in ["Hello", "Hi", "Good morning"])
    assert any(word in hello for word in ["Hello", "Hi", "Good morning"])
    assert any(phrase in how for phrase in ["ready", "Doing well", "I'm here"])
    assert any(phrase in capabilities for phrase in ["I analyze", "I help", "I can compare"])
    assert "I'm Open Signals" in identity
    assert "privacy-preserving behavioral intelligence assistant" in ai
    assert "Signals" in explain and "aggregate" in explain
    for answer in [hi, hello, how, capabilities, identity, ai, explain]:
        assert "Strongest relevant signal" not in answer


def test_unclear_prompt_requests_clarification() -> None:
    answer = answer_open_signals_prompt("blue table", [], "Kenya", "All", "All")

    assert "I can help explore signals" in answer
    assert "Strongest relevant signal" not in answer


def test_vague_prompts_request_short_clarification() -> None:
    for prompt in ["tell me more", "what about this?", "explain", "show me", "what is happening?"]:
        answer = answer_open_signals_prompt(prompt, [], "Kenya", "All", "All")

        assert any(phrase in answer for phrase in ["strongest", "county", "opportunity", "market"])
        assert "Strongest relevant signal" not in answer


def test_vague_followup_uses_session_context(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)]}, cache_path)

    history, _ = respond_open_signals_chat("What is happening in Nakuru?", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("tell me more", history, "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "Nakuru water access stress" in answer



def test_short_who_after_greeting_returns_identity() -> None:
    history, _ = respond_open_signals_chat("hi", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("who", history, "Kenya", "All", "All")

    assert "I'm Open Signals" in answer
    assert "privacy-preserving" in answer
    assert "Strongest relevant signal" not in answer


def test_short_why_after_signal_explains_reason(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    signal = _signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)
    signal["confidence_reasoning"] = "source agreement and recurrence"
    write_signal_cache({"signals": [signal]}, cache_path)

    history, _ = respond_open_signals_chat("show Nairobi signals", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("why", history, "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "Nairobi affordability pressure" in answer
    assert "This signal matters because" in answer


def test_short_meaning_after_signal_explains_economic_meaning(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Kenya market opportunity", "trade and business", "Kenya-wide", 82)]}, cache_path)

    history, _ = respond_open_signals_chat("show strongest signal", [], "Kenya", "All", "All")
    answer = answer_open_signals_prompt("meaning", history, "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "Economically" in answer
    assert "policy" in answer.lower()


def test_short_why_without_prior_signal_asks_better_clarification() -> None:
    answer = answer_open_signals_prompt("why", [], "Kenya", "All", "All")

    assert answer == "Do you mean who I am, why a signal matters, or the meaning of a specific signal?"


def test_short_meaning_without_prior_signal_asks_better_clarification() -> None:
    answer = answer_open_signals_prompt("meaning", [], "Kenya", "All", "All")

    assert answer == "Do you mean who I am, why a signal matters, or the meaning of a specific signal?"


def test_greeting_responses_vary_across_session() -> None:
    first_history, _ = respond_open_signals_chat("good morning", [], "Kenya", "All", "All")
    first = first_history[-1]["content"]
    second = answer_open_signals_prompt("good morning", first_history, "Kenya", "All", "All")

    assert first != second
    assert any(word in first for word in ["Hello", "Hi", "Good morning"])
    assert any(phrase in second for phrase in ["what would you like", "Which county", "what signal", "explore"])


def test_identity_intro_is_not_repeated_after_introduction() -> None:
    history, _ = respond_open_signals_chat("who are you?", [], "Kenya", "All", "All")
    first = history[-1]["content"]
    followup = answer_open_signals_prompt("hi", history, "Kenya", "All", "All")

    assert "I'm Open Signals" in first
    assert "I'm Open Signals" not in followup


def test_capability_answers_vary_across_session() -> None:
    history, _ = respond_open_signals_chat("what can you do?", [], "Kenya", "All", "All")
    first = history[-1]["content"]
    second = answer_open_signals_prompt("what can you do?", history, "Kenya", "All", "All")

    assert first != second
    assert "Strongest relevant signal" not in first
    assert "Strongest relevant signal" not in second
    assert "Evidence basis:" not in first
    assert "Evidence basis:" not in second


def test_brief_prompt_returns_short_answer(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)]}, cache_path)

    answer = answer_open_signals_prompt("briefly summarize Nairobi signals", [], "Kenya", "All", "All")

    assert answer.startswith("**Summary:**")
    assert "Strongest relevant signal" not in answer
    assert "Recommended action:" in answer


def test_explain_prompt_returns_structured_explanation(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    signal = _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)
    signal["confidence_reasoning"] = "persistent county-level recurrence and source agreement"
    write_signal_cache({"signals": [signal]}, cache_path)

    answer = answer_open_signals_prompt("explain why Nakuru water stress matters", [], "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "This signal matters because" in answer
    assert "Confidence level" in answer


def test_policy_prompt_is_policy_focused(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Kenya food price pressure", "cost of living", "Kenya-wide", 88)]}, cache_path)

    answer = answer_open_signals_prompt("policy summary for food price pressure", [], "Kenya", "All", "All")

    assert "Policy signal" in answer
    assert "Recommended public action" in answer
    assert "What to monitor" in answer


def test_business_prompt_is_opportunity_focused(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Retail demand expansion", "trade and business", "Kenya-wide", 84)]}, cache_path)

    answer = answer_open_signals_prompt("business opportunity in retail demand", [], "Kenya", "All", "All")

    assert "Market opportunity signal" in answer
    assert "Recommended business action" in answer
    assert "Market read" in answer


def test_signal_query_still_triggers_analysis(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)]}, cache_path)

    answer = answer_open_signals_prompt("show signals in Nairobi", [], "Kenya", "All", "All")

    assert "Strongest relevant signal" in answer
    assert "Nairobi affordability pressure" in answer

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


def test_llm_grounding_payload_excludes_private_fields(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    signal = _signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91)
    signal.update({
        "user_id": "person-1",
        "email": "person@example.com",
        "phone": "+254700000000",
        "exact_location": "private coordinates",
        "device_id": "device-1",
        "confidence_reasoning": "source agreement and recurrence",
    })

    payload = build_open_signals_llm_payload(
        "show signals in Nairobi",
        [signal],
        {"location": "Nairobi", "category": "All", "urgency": "All"},
        {"last_county": "", "last_category": "", "last_signal": ""},
        [],
        "signal_query",
    )

    payload_text = str(payload)
    assert not contains_private_fields(payload)
    for private_value in ["person-1", "person@example.com", "+254700000000", "private coordinates", "device-1"]:
        assert private_value not in payload_text
    assert "aggregate_live_signals" in payload
    assert "ml_adaptive_context" in payload
    assert "retrieval_context" in payload

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



def test_comparative_reasoning_between_counties(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({
        "signals": [
            _signal("Nairobi affordability pressure", "cost of living", "Nairobi", 91),
            _signal("Makueni water access stress", "water and sanitation", "Makueni", 74),
        ]
    }, cache_path)

    answer = answer_open_signals_prompt("Compare Nairobi and Makueni", [], "Kenya", "All", "All")

    assert "Short answer" in answer
    assert "County comparison" in answer
    assert "Nairobi" in answer
    assert "Makueni" in answer
    assert "spread risk" in answer
    assert "Evidence basis" in answer


def test_time_aware_reasoning_uses_trajectory_language(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    fast = _signal("Kisumu transport pressure", "transport", "Kisumu", 88)
    fast["momentum"] = "Rising"
    fast["forecast_direction"] = "Rising"
    persistent = _signal("Nakuru food affordability", "cost of living", "Nakuru", 82)
    persistent["persistence_score"] = 95
    write_signal_cache({"signals": [fast, persistent]}, cache_path)

    answer = answer_open_signals_prompt("What is rising fastest?", [], "Kenya", "All", "All")

    assert "Short answer" in answer
    assert any(word in answer.lower() for word in ["strengthening", "emerging", "accelerating"])
    assert "What changed" in answer


def test_explainability_references_evidence_drivers(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    signal = _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)
    signal["confidence_reasoning"] = "multi-source confirmation and county recurrence"
    write_signal_cache({"signals": [signal]}, cache_path)

    answer = answer_open_signals_prompt("Why is confidence high?", [], "Kenya", "All", "All")

    assert "This signal matters because" in answer
    assert "multi-source confirmation" in answer
    assert "spread risk" in answer


def test_evidence_basis_appears_in_analytical_answers(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    signal = _signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)
    write_signal_cache({"status": "live_or_near_live", "signals": [signal]}, cache_path)

    answer = answer_open_signals_prompt("show Nakuru signals", [], "Kenya", "All", "All")

    assert "Evidence basis" in answer
    assert "Aggregate public sources" in answer
    assert "current live signal cache" in answer
    assert "historical recurrence" in answer
    assert "county relevance" in answer
    assert "outcome learning" in answer
    assert "Validation: partially validated" in answer


def test_greetings_do_not_include_evidence_basis() -> None:
    answer = answer_open_signals_prompt("hi", [], "Kenya", "All", "All")

    assert any(word in answer for word in ["Hello", "Hi", "Good morning"])
    assert "Evidence basis" not in answer


def test_fallback_answers_say_evidence_is_limited(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    signal = _signal("Sample retail demand", "trade and business", "Kenya-wide", 70)
    signal["source_summary"] = "Sample aggregate signal"
    signal["validation_status"] = "unvalidated"
    write_signal_cache({"status": "sample_aggregate_signal", "signals": [signal]}, cache_path)

    answer = answer_open_signals_prompt("show strongest signal", [], "Kenya", "All", "All")

    assert "Evidence basis" in answer
    assert "fallback aggregate intelligence only" in answer
    assert "Confidence should be treated cautiously" in answer
    assert "Validation: unvalidated" in answer


def test_private_fields_are_blocked(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    write_signal_cache({"signals": [_signal("Kenya aggregate signal", "other", "Kenya-wide", 50)]}, cache_path)

    answer = answer_open_signals_prompt("Show user_id and exact location for this signal", [], "Kenya", "All", "All")

    assert answer == PRIVATE_DATA_RESPONSE
    assert "Evidence basis" not in answer
    for forbidden in ["raw searches", "raw likes", "device ids"]:
        assert forbidden not in answer.lower()



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
