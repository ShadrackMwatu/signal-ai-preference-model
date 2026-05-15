from pathlib import Path


def test_app_import_and_kenya_ui_function():
    import app

    feed, emerging, interpretation, historical = app.get_kenya_live_signals_for_ui("Kenya", "All", "All")
    assert "signal-card" in feed
    assert "Emerging Kenya Signals" in emerging
    assert "Detected from:" in interpretation
    assert "Historical Learning Insight" in historical


def test_behavioral_ui_has_no_refresh_or_raw_labels():
    source = Path("app.py").read_text(encoding="utf-8")
    forbidden = [
        "Refresh Signals",
        'label="Likes"',
        'label="Comments"',
        'label="Shares"',
        'label="Searches"',
        "Engagement Intensity",
        "Purchase Intent",
        "Demo fallback",
    ]
    for text in forbidden:
        assert text not in source


def test_kenya_signal_fusion_returns_valid_signals():
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals

    signals = fuse_kenya_signals("Kenya", "All", "All")
    assert signals
    first = signals[0]
    for key in [
        "signal_topic",
        "signal_category",
        "demand_level",
        "opportunity_level",
        "unmet_demand_likelihood",
        "urgency",
        "geographic_scope",
        "source_summary",
        "confidence_score",
        "last_updated",
        "interpretation",
        "recommended_action",
    ]:
        assert key in first
    assert first["demand_level"] in {"Low", "Moderate", "High"}
    assert first["privacy_level"] == "aggregate_public"


def test_county_detection_works():
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import detect_county

    assert detect_county("water shortage Makueni") == "Makueni"
    assert detect_county("jobs in Nairobi") == "Nairobi"
    assert detect_county("maize flour prices") == "Kenya-wide"


def test_missing_credentials_do_not_crash(monkeypatch):
    for key in ["SERPAPI_KEY", "NEWS_API_KEY", "YOUTUBE_API_KEY", "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "X_BEARER_TOKEN"]:
        monkeypatch.delenv(key, raising=False)
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals

    signals = fuse_kenya_signals("Kenya", "All", "All")
    assert signals


def test_source_summary_hides_private_data():
    from Behavioral_Signals_AI.privacy import sanitize_aggregate_record
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals

    sanitized = sanitize_aggregate_record({"topic": "health", "user_id": "123", "email": "x@y.com"})
    assert "user_id" not in sanitized
    assert "email" not in sanitized
    signal = fuse_kenya_signals("Kenya", "All", "All")[0]
    assert "user_id" not in signal.get("source_summary", "")
    assert "email" not in signal.get("source_summary", "")


def test_signal_cge_tab_remains_present():
    source = Path("app.py").read_text(encoding="utf-8")
    assert 'with gr.Tab("Signal CGE")' in source