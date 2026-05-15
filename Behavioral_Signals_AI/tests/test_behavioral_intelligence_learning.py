from pathlib import Path

from Behavioral_Signals_AI.signal_engine.behavioral_learning_engine import load_behavioral_memory, update_behavioral_learning
from Behavioral_Signals_AI.signal_engine.behavioral_signal_taxonomy import classify_behavioral_families


def _signal(topic="cheap maize flour near me", **extra):
    payload = {
        "signal_topic": topic,
        "semantic_cluster": topic,
        "signal_category": "food and agriculture",
        "demand_level": "Moderate",
        "opportunity_level": "Moderate",
        "unmet_demand_likelihood": "Medium",
        "geographic_scope": "Kenya-wide",
        "source_summary": "Search Trends",
        "momentum": "Rising",
        "confidence_score": 50,
        "priority_score": 55,
        "multi_source_confirmation_score": 35,
        "noise_level": 5,
        "privacy_level": "aggregate_public",
    }
    payload.update(extra)
    return payload


def test_behavioral_family_classification():
    assert "Demand" in classify_behavioral_families(_signal("where to buy affordable smartphones near me"))
    assert "Affordability" in classify_behavioral_families(_signal("cheap smartphones price and pay later"))
    assert "Stress" in classify_behavioral_families(_signal("water shortage urgent hospital near me"))
    assert "Opportunity" in classify_behavioral_families(_signal("county-specific shortage and supply gap"))


def test_repeated_signals_increase_behavioral_intelligence(tmp_path):
    path = tmp_path / "behavioral_memory.json"
    first = update_behavioral_learning(_signal("maize flour prices"), [{"source_type": "search_trend", "topic": "maize flour prices"}], path=path)
    second = update_behavioral_learning(_signal("maize flour prices"), [{"source_type": "search_trend", "topic": "maize flour prices"}], path=path)
    assert second["behavioral_intelligence_score"] >= first["behavioral_intelligence_score"]
    assert second["persistence_score"] > first["persistence_score"]


def test_multi_source_confirmation_and_geographic_spread_increase_scores(tmp_path):
    path = tmp_path / "behavioral_memory.json"
    one = update_behavioral_learning(
        _signal("fuel prices", geographic_scope="Nairobi"),
        [{"source_type": "search_trend", "topic": "fuel prices"}],
        path=path,
    )
    two = update_behavioral_learning(
        _signal("fuel prices", geographic_scope="Mombasa", multi_source_confirmation_score=80),
        [{"source_type": "search_trend", "topic": "fuel prices"}, {"source_type": "public_news", "topic": "fuel prices"}],
        path=path,
    )
    assert two["cross_source_confirmation_score"] >= one["cross_source_confirmation_score"]
    assert two["geographic_spread_score"] >= one["geographic_spread_score"]


def test_one_off_signal_remains_conservative(tmp_path):
    signal = update_behavioral_learning(
        _signal("vague topic", confidence_score=40, priority_score=38, multi_source_confirmation_score=20),
        [{"source_type": "single_source", "topic": "vague topic"}],
        path=tmp_path / "behavioral_memory.json",
    )
    assert signal["behavioral_intelligence_score"] < 60
    assert "one-off" in signal["adaptation_note"] or "source-limited" in signal["adaptation_note"]


def test_historical_recurrence_improves_adaptation_note(tmp_path):
    signal = update_behavioral_learning(
        _signal("school fees high cost", historical_pattern_match="Similar to prior cost signal"),
        [{"source_type": "search_trend", "topic": "school fees high cost"}, {"source_type": "public_news", "topic": "school fees"}],
        path=tmp_path / "behavioral_memory.json",
    )
    assert signal["historical_recurrence_score"] >= 55
    assert "historical" in signal["adaptation_note"].lower()


def test_behavioral_memory_initializes_and_recovers_from_malformed(tmp_path):
    path = tmp_path / "behavioral_memory.json"
    path.write_text("{bad json", encoding="utf-8")
    memory = load_behavioral_memory(path)
    assert memory["clusters"] == {}
    updated = update_behavioral_learning(_signal("jobs in Nairobi"), [], path=path)
    assert updated["behavioral_families"]


def test_ui_does_not_expose_personal_or_raw_behavioral_data():
    from Behavioral_Signals_AI.signal_engine.kenya_ui import render_strategic_interpretation

    html = render_strategic_interpretation([update_behavioral_learning(_signal("cheap smartphones"), [])])
    lowered = html.lower()
    assert "behavioral intelligence" in lowered
    for forbidden in ["user_id", "email", "phone", "private message", "individual profile"]:
        assert forbidden not in lowered


def test_app_import_and_signal_cge_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source
