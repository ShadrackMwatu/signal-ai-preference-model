from pathlib import Path

from Behavioral_Signals_AI.ui.feed_diff_engine import has_material_signal_change, rank_signals_for_display


def _signal(topic, **extra):
    payload = {
        "signal_topic": topic,
        "semantic_cluster": topic,
        "urgency": "Medium",
        "momentum": "Stable",
        "forecast_direction": "Stable",
        "confidence_score": 60,
        "behavioral_intelligence_score": 60,
        "persistence_score": 55,
        "multi_source_confirmation_score": 50,
        "geographic_spread_score": 45,
        "historical_recurrence_score": 40,
        "historical_accuracy_score": 50,
    }
    payload.update(extra)
    return payload


def test_green_live_status_dot_exists_beside_behavioral_heading():
    source = Path("app.py").read_text(encoding="utf-8")
    assert "class='behavioral-heading'" in source
    assert "Behavioral Signals AI " in source
    assert "class='live-status-dot'" in source
    assert "Live signal intelligence updating" in source


def test_only_dot_has_blinking_animation_not_feed_container():
    source = Path("app.py").read_text(encoding="utf-8")
    assert ".live-status-dot" in source
    assert "animation: signalPulse 1s infinite ease-in-out" in source
    assert "@keyframes signalPulse" in source
    feed_block = source[source.index(".signal-feed-container {"):source.index(".signal-card {")]
    assert "signalPulse" not in feed_block
    assert "opacity:" not in feed_block
    heading_block = source[source.index(".behavioral-heading {"):source.index(".live-status-dot {")]
    assert "animation:" not in heading_block


def test_unchanged_signals_do_not_trigger_full_feed_rebuild(monkeypatch):
    from Behavioral_Signals_AI.signal_engine import kenya_ui

    kenya_ui.reset_live_feed_render_cache()
    payload_one = {"last_updated": "t1", "signals": [_signal("maize flour prices")]}
    payload_two = {"last_updated": "t2", "signals": [_signal("maize flour prices")]}
    calls = iter([payload_one, payload_two])
    monkeypatch.setattr(kenya_ui, "get_cached_or_fallback_signals", lambda: next(calls))
    first = kenya_ui.get_kenya_live_signals_for_ui("Kenya", "All", "All")
    second = kenya_ui.get_kenya_live_signals_for_ui("Kenya", "All", "All")
    assert first == second
    assert "Last updated: t1" in first[0]


def test_material_ranking_changes_trigger_feed_update(monkeypatch):
    from Behavioral_Signals_AI.signal_engine import kenya_ui

    kenya_ui.reset_live_feed_render_cache()
    first_payload = {"last_updated": "t1", "signals": [_signal("maize flour prices", confidence_score=70), _signal("fuel prices", confidence_score=50)]}
    second_payload = {"last_updated": "t2", "signals": [_signal("maize flour prices", confidence_score=55), _signal("fuel prices", confidence_score=90, urgency="High", momentum="Breakout", forecast_direction="Rising")]}
    calls = iter([first_payload, second_payload])
    monkeypatch.setattr(kenya_ui, "get_cached_or_fallback_signals", lambda: next(calls))
    first = kenya_ui.get_kenya_live_signals_for_ui("Kenya", "All", "All")
    second = kenya_ui.get_kenya_live_signals_for_ui("Kenya", "All", "All")
    assert first != second
    assert second[0].find("fuel prices") < second[0].find("maize flour prices")


def test_feed_diff_engine_material_change_rules():
    previous = [_signal("maize flour prices"), _signal("fuel prices")]
    assert not has_material_signal_change(previous, [_signal("maize flour prices"), _signal("fuel prices")])
    assert has_material_signal_change(previous, [_signal("fuel prices"), _signal("maize flour prices")])
    assert has_material_signal_change(previous, [_signal("maize flour prices", confidence_score=67), _signal("fuel prices")])
    assert has_material_signal_change(previous, [_signal("maize flour prices", momentum="Rising"), _signal("fuel prices")])


def test_top_signal_can_be_overtaken_by_stronger_emerging_signal():
    ranked = rank_signals_for_display([
        _signal("maize flour prices", confidence_score=65, behavioral_intelligence_score=60),
        _signal("fuel prices", confidence_score=92, behavioral_intelligence_score=95, urgency="High", momentum="Breakout", forecast_direction="Rising", multi_source_confirmation_score=90),
    ])
    assert ranked[0]["signal_topic"] == "fuel prices"


def test_app_import_and_signal_cge_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert 'with gr.Tab("Signal CGE")' in source