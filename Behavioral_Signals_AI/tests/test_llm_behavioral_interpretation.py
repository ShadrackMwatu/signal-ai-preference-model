from pathlib import Path

from Behavioral_Signals_AI.llm.safety_guardrails import contains_private_fields, sanitize_llm_signal_input
from Behavioral_Signals_AI.llm.signal_interpreter import REQUIRED_INTERPRETATION_FIELDS, interpret_signal_with_llm
from Behavioral_Signals_AI.llm.strategic_summary import generate_strategic_signal_summary


def _signal(**extra):
    payload = {
        "signal_topic": "maize flour prices",
        "signal_category": "food and agriculture",
        "geographic_scope": "Kenya-wide",
        "behavioral_families": ["Demand", "Affordability"],
        "momentum": "Rising",
        "confidence_score": 78,
        "source_summary": "Search Trends + Public News",
        "historical_pattern_match": "Food affordability pressure",
        "outcome_learning_note": "Historically, similar signals have often preceded food affordability pressure.",
        "demand_level": "High",
        "opportunity_level": "Moderate",
        "privacy_level": "aggregate_public",
    }
    payload.update(extra)
    return payload


def test_llm_disabled_fallback_returns_required_fields(monkeypatch):
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    result = interpret_signal_with_llm(_signal())
    for field in REQUIRED_INTERPRETATION_FIELDS:
        assert result[field]
    assert result["llm_mode"] == "rule_based_fallback"


def test_missing_api_key_does_not_crash(monkeypatch):
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "true")
    monkeypatch.delenv("SIGNAL_LLM_API_KEY", raising=False)
    result = interpret_signal_with_llm(_signal())
    assert result["plain_language_meaning"]
    assert result["llm_mode"] == "rule_based_fallback"


def test_private_fields_removed_before_llm_call():
    safe = sanitize_llm_signal_input(_signal(user_id="abc", email="x@example.com", phone="123", private_message="secret"))
    assert not contains_private_fields(safe)
    assert "user_id" not in safe
    assert "email" not in safe
    assert safe["privacy_instruction"] == "aggregate_public_or_authorized_only_no_individual_profiling"


def test_strategic_summary_returns_non_empty_text(monkeypatch):
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    summary = generate_strategic_signal_summary([_signal(), _signal(signal_topic="fuel prices", signal_category="transport")])
    assert isinstance(summary, str)
    assert "Main issue emerging" in summary


def test_kenya_fusion_attaches_llm_fields(monkeypatch):
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import _llm_interpretation_fields

    fields = _llm_interpretation_fields(_signal())
    assert fields["plain_language_meaning"]
    assert fields["llm_input_privacy"] == "aggregate_sanitized"
    assert fields["recommended_action"]


def test_public_ui_contains_ai_assisted_note_and_no_raw_prompt():
    source = Path("app.py").read_text(encoding="utf-8")
    assert "Interpretations are AI-assisted and based on aggregate signal patterns" in source
    assert "raw prompt" not in source.lower()


def test_app_import_and_signal_cge_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert 'with gr.Tab("Signal CGE")' in source