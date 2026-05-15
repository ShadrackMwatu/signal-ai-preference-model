import json
from pathlib import Path


def test_app_uses_content_timer_for_signal_panels():
    source = Path("app.py").read_text(encoding="utf-8")
    assert "content_timer = gr.Timer(value=30)" in source
    assert "ui_timer = gr.Timer(value=1)" not in source


def test_ui_renderer_reads_cache_only_not_heavy_collection():
    source = Path("Behavioral_Signals_AI/signal_engine/kenya_ui.py").read_text(encoding="utf-8")
    assert "fuse_kenya_signals" not in source
    assert "get_cached_or_fallback_signals" in source


def test_latest_live_signal_cache_is_used_when_available(tmp_path, monkeypatch):
    cache_path = tmp_path / "latest_live_signals.json"
    payload = {
        "last_updated": "2026-05-15T10:00:00+03:00",
        "status": "cached",
        "privacy_level": "aggregate_public",
        "signals": [
            {
                "signal_topic": "cached maize affordability signal",
                "signal_category": "food and agriculture",
                "demand_level": "High",
                "opportunity_level": "Moderate",
                "unmet_demand_likelihood": "High",
                "urgency": "High",
                "geographic_scope": "Kenya-wide",
                "source_summary": "Cached aggregate signal",
                "confidence_score": 81,
                "last_updated": "2026-05-15T10:00:00+03:00",
                "recommended_action": "Monitor affordability pressure.",
                "momentum": "Rising",
                "privacy_level": "aggregate_public",
            }
        ],
    }
    cache_path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))

    from Behavioral_Signals_AI.signal_engine.kenya_ui import get_kenya_live_signals_for_ui

    feed, emerging, interpretation, historical = get_kenya_live_signals_for_ui("Kenya", "All", "All")
    assert "cached maize affordability signal" in feed
    assert "Source intelligence updated: 2026-05-15T10:00:00+03:00" in feed
    assert feed.strip()
    assert emerging.strip()
    assert interpretation.strip()
    assert historical.strip()


def test_feed_never_renders_blank_with_missing_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(tmp_path / "missing.json"))
    from Behavioral_Signals_AI.signal_engine.kenya_ui import get_kenya_live_signals_for_ui

    outputs = get_kenya_live_signals_for_ui("Kenya", "All", "All")
    assert len(outputs) == 4
    assert all(str(output).strip() for output in outputs)


def test_background_collection_interval_is_not_one_second_by_default():
    source = Path("Behavioral_Signals_AI/signal_engine/background_signal_service.py").read_text(encoding="utf-8")
    assert 'SIGNAL_BACKGROUND_POLL_SECONDS", "60"' in source
    assert "return max(15" in source


def test_app_import_and_signal_cge_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source
