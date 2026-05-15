from pathlib import Path


def test_live_feed_html_never_empty():
    from Behavioral_Signals_AI.signal_engine.kenya_ui import render_live_signal_feed, render_emerging_signals, render_strategic_interpretation

    assert "signal-card" in render_live_signal_feed([])
    assert "Live Kenya signal stream" in render_live_signal_feed([])
    assert render_emerging_signals([]).strip()
    assert render_strategic_interpretation([]).strip()


def test_cache_initializes_if_missing(tmp_path, monkeypatch):
    cache_file = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_file))
    from Behavioral_Signals_AI.signal_engine.signal_cache import initialize_signal_cache

    payload = initialize_signal_cache()
    assert cache_file.exists()
    assert payload["signals"]
    assert payload["last_updated"]


def test_cached_signals_are_used_when_collection_fails(tmp_path, monkeypatch):
    cache_file = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_file))
    from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache, refresh_signal_cache
    import Behavioral_Signals_AI.signal_engine.signal_cache as signal_cache

    write_signal_cache({"last_updated": "cached", "signals": [{"signal_topic": "cached topic", "signal_category": "other"}]})
    monkeypatch.setattr(signal_cache, "fuse_kenya_signals", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")))
    payload = refresh_signal_cache()
    assert payload["signals"][0]["signal_topic"] == "cached topic"
    assert payload["status"] == "using_cached_last_success"


def test_fallback_used_when_cache_missing(tmp_path, monkeypatch):
    cache_file = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_file))
    from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals

    payload = get_cached_or_fallback_signals()
    assert payload["signals"]
    assert cache_file.exists()


def test_background_service_does_not_start_duplicate_threads(monkeypatch, tmp_path):
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(tmp_path / "latest_live_signals.json"))
    monkeypatch.setenv("SIGNAL_BACKGROUND_POLL_SECONDS", "60")
    monkeypatch.setenv("SIGNAL_BACKGROUND_SERVICE_ENABLED", "true")
    from Behavioral_Signals_AI.signal_engine.background_signal_service import start_background_signal_service, service_status

    first = start_background_signal_service()
    second = start_background_signal_service()
    status = service_status()
    assert status["running"]
    assert first in {True, False}
    assert second is False


def test_gradio_timer_reads_cache_path_instead_of_collecting_directly():
    source = Path("app.py").read_text(encoding="utf-8")
    assert "ui_timer = gr.Timer(value=1)" in source
    assert "fn=get_kenya_live_signals_for_ui" in source
    assert "refresh_signal_cache" not in source


def test_raw_labels_remain_hidden_and_signal_cge_present():
    source = Path("app.py").read_text(encoding="utf-8")
    for text in ["Refresh Signals", 'label="Likes"', 'label="Comments"', 'label="Shares"', 'label="Searches"', "Engagement Intensity", "Purchase Intent", "Demo fallback"]:
        assert text not in source
    assert 'with gr.Tab("Signal CGE")' in source