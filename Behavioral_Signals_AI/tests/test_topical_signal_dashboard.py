from pathlib import Path


def test_topical_signal_generator_returns_feed_and_interpretation():
    from app import get_topical_signals_for_ui

    feed_html, interpretation = get_topical_signals_for_ui("Kenya", "All", "All", "All")
    assert "signal-card" in feed_html
    assert "Signal Interpretation & Opportunity" in interpretation
    assert "Signal uses aggregate" in interpretation


def test_app_source_hides_raw_behavioral_inputs():
    source = Path("app.py").read_text(encoding="utf-8")
    forbidden = [
        "Refresh Signals",
        'label="Likes"',
        'label="Comments"',
        'label="Shares"',
        'label="Searches"',
        "Engagement Intensity",
        "Purchase Intent",
        "Trend Growth",
        "Demo fallback",
    ]
    for text in forbidden:
        assert text not in source


def test_missing_credentials_do_not_crash(monkeypatch):
    for key in [
        "GOOGLE_TRENDS_ENABLED",
        "YOUTUBE_API_KEY",
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "X_BEARER_TOKEN",
        "GOOGLE_ANALYTICS_PROPERTY_ID",
        "SIGNAL_DATA_MODE",
    ]:
        monkeypatch.delenv(key, raising=False)
    from Behavioral_Signals_AI.signal_engine.topical_signal_generator import generate_topical_signals

    signals = generate_topical_signals("Kenya", "All", "All", "All")
    assert signals
    assert all(signal["privacy_level"] == "aggregate_public" for signal in signals)


def test_privacy_guardrails_block_individual_fields():
    from Behavioral_Signals_AI.privacy import sanitize_aggregate_record, validate_privacy_safe_record

    record = {
        "topic": "hospital near me",
        "user_id": "abc",
        "email": "person@example.com",
        "phone": "+254700000000",
        "private_message": "private",
        "exact_location": "private coordinates",
        "personal_profile": "profile",
    }
    is_safe, blocked = validate_privacy_safe_record(record)
    assert not is_safe
    assert {"user_id", "email", "phone", "private_message", "exact_location", "personal_profile"}.issubset(set(blocked))
    sanitized = sanitize_aggregate_record(record)
    assert "user_id" not in sanitized
    assert "email" not in sanitized
    assert sanitized["privacy_level"] == "aggregate_public"


def test_signal_cge_tab_still_present():
    source = Path("app.py").read_text(encoding="utf-8")
    assert 'with gr.Tab("Signal CGE")' in source