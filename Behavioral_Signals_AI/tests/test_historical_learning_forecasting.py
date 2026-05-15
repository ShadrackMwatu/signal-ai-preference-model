import importlib
from pathlib import Path


def _reload_history_modules(monkeypatch, tmp_path):
    monkeypatch.setenv("SIGNAL_HISTORICAL_MEMORY_PATH", str(tmp_path / "historical_signal_memory.json"))
    monkeypatch.setenv("SIGNAL_HISTORICAL_INSIGHT_INDEX_PATH", str(tmp_path / "historical_insight_index.json"))
    monkeypatch.setenv("SIGNAL_FORECAST_MEMORY_PATH", str(tmp_path / "forecast_memory.json"))
    monkeypatch.setenv("SIGNAL_HISTORY_ROOT", str(tmp_path / "history"))
    import Behavioral_Signals_AI.signal_engine.historical_memory as historical_memory
    import Behavioral_Signals_AI.signal_engine.daily_learning_engine as daily_learning_engine
    import Behavioral_Signals_AI.signal_engine.monthly_learning_engine as monthly_learning_engine
    import Behavioral_Signals_AI.signal_engine.yearly_learning_engine as yearly_learning_engine
    import Behavioral_Signals_AI.signal_engine.historical_adaptation_engine as historical_adaptation_engine
    import Behavioral_Signals_AI.signal_engine.historical_forecasting_engine as historical_forecasting_engine

    for module in [
        historical_memory,
        daily_learning_engine,
        monthly_learning_engine,
        yearly_learning_engine,
        historical_adaptation_engine,
        historical_forecasting_engine,
    ]:
        importlib.reload(module)
    return historical_memory, daily_learning_engine, monthly_learning_engine, yearly_learning_engine, historical_adaptation_engine, historical_forecasting_engine


def _sample_signal():
    return {
        "signal_topic": "Food affordability pressure",
        "semantic_cluster": "Food affordability pressure",
        "signal_category": "food and agriculture",
        "geographic_scope": "Kenya-wide",
        "demand_intelligence_score": 78,
        "opportunity_intelligence_score": 68,
        "urgency_score": 82,
        "confidence_score": 74,
        "momentum": "Rising",
        "validation_status": "partially_validated",
        "forecast_confidence": 70,
        "predicted_direction": "rising",
        "confidence_reasoning": "Confidence adjusted because aggregate evidence persists.",
    }


def test_daily_monthly_yearly_history_files_are_created(monkeypatch, tmp_path):
    _, daily, monthly, yearly, _, _ = _reload_history_modules(monkeypatch, tmp_path)
    signals = [_sample_signal()]
    daily_summary = daily.summarize_daily_signals(signals, date="2026-05-15")
    monthly_summary = monthly.summarize_monthly_patterns("2026-05")
    yearly_summary = yearly.summarize_yearly_patterns("2026")

    assert (tmp_path / "history" / "daily" / "2026-05-15.json").exists()
    assert (tmp_path / "history" / "monthly" / "2026-05.json").exists()
    assert (tmp_path / "history" / "yearly" / "2026.json").exists()
    assert daily_summary["top_signals"]
    assert monthly_summary["recurring_themes"]
    assert yearly_summary["major_national_demand_shifts"]


def test_missing_and_malformed_history_recover_safely(monkeypatch, tmp_path):
    history, _, _, _, _, _ = _reload_history_modules(monkeypatch, tmp_path)
    malformed = tmp_path / "historical_signal_memory.json"
    malformed.write_text("{bad json", encoding="utf-8")
    payload = history.load_json(malformed, {"records": []})
    assert payload == {"records": []}
    history.initialize_history_stores()
    assert (tmp_path / "historical_insight_index.json").exists()


def test_historical_pattern_matching_and_forecast_fields(monkeypatch, tmp_path):
    history, daily, _, _, adaptation, forecasting = _reload_history_modules(monkeypatch, tmp_path)
    signal = _sample_signal()
    daily.summarize_daily_signals([signal], date="2026-05-15")
    adapted = adaptation.apply_historical_adaptation(signal)
    forecasted = forecasting.add_historical_forecast(adapted)

    assert forecasted["historical_pattern_match"] != "No close historical pattern yet"
    assert forecasted["forecast_direction"] in {"Rising", "Stable", "Declining"}
    assert forecasted["forecast_confidence"] >= signal["forecast_confidence"]
    assert forecasted["forecast_reasoning"]
    assert forecasted["historical_lesson_used"]
    history.append_forecast_memory([forecasted])
    assert (tmp_path / "forecast_memory.json").exists()


def test_historical_lessons_influence_scoring(monkeypatch, tmp_path):
    _, daily, _, _, adaptation, _ = _reload_history_modules(monkeypatch, tmp_path)
    signal = _sample_signal()
    daily.summarize_daily_signals([{**signal, "future_relevance": "High"}], date="2026-05-15")
    adapted = adaptation.apply_historical_adaptation({**signal, "confidence_score": 60})
    assert adapted["confidence_score"] >= 60
    assert "historical_lesson_used" in adapted


def test_public_ui_historical_insight_hides_raw_behavioral_data():
    from Behavioral_Signals_AI.signal_engine.kenya_ui import render_strategic_interpretation

    html = render_strategic_interpretation([_sample_signal()])
    assert "Historical Learning Insight" in html
    lowered = html.lower()
    for forbidden in ["likes", "comments", "shares", "private_message", "user_id", "email"]:
        assert forbidden not in lowered


def test_app_import_and_signal_cge_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source
