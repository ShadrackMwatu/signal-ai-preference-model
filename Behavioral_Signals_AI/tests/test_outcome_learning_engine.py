from pathlib import Path

from Behavioral_Signals_AI.signal_engine.kenya_ui import render_strategic_interpretation
from Behavioral_Signals_AI.signal_engine.outcome_learning_engine import (
    apply_outcome_learning,
    initialize_outcome_memory,
    load_outcome_memory,
    recognized_follow_up_windows,
)


def _signal(topic="maize flour prices", **extra):
    payload = {
        "signal_topic": topic,
        "semantic_cluster": topic,
        "signal_category": "food and agriculture",
        "demand_level": "High",
        "opportunity_level": "Moderate",
        "confidence_score": 50,
        "source_reliability_score": 55,
        "category_confidence_score": 55,
        "forecast_direction": "Rising",
        "predicted_direction": "rising",
        "recommended_action": "Monitor food affordability pressure using aggregate public evidence.",
        "privacy_level": "aggregate_public",
        "last_updated": "2026-05-15T00:00:00+00:00",
    }
    payload.update(extra)
    return payload


def test_outcome_memory_initialization(tmp_path):
    path = tmp_path / "outcome_learning_memory.json"
    memory = initialize_outcome_memory(path)
    assert memory["clusters"] == {}
    assert memory["follow_up_windows_days"] == [7, 30, 90, 365]
    assert path.exists()


def test_confirmed_outcome_improves_future_confidence(tmp_path):
    path = tmp_path / "outcome_learning_memory.json"
    confirmed = apply_outcome_learning(
        _signal(confidence_score=50),
        evidence={
            "outcome_status": "confirmed",
            "observed_outcome": "Official and public aggregate evidence later confirmed food affordability pressure.",
            "accuracy_score": 90,
            "evidence_sources": ["official statistics", "public news follow-up"],
        },
        path=path,
    )
    assert confirmed["outcome_learning_status"] == "historically_confirmed"
    assert confirmed["confidence_score"] > 50
    future = apply_outcome_learning(_signal(confidence_score=50), path=path)
    assert future["outcome_learning_status"] == "historically_confirmed"
    assert future["confidence_score"] > 50


def test_unconfirmed_outcome_reduces_future_confidence(tmp_path):
    path = tmp_path / "outcome_learning_memory.json"
    weak = apply_outcome_learning(
        _signal("brief vague signal", confidence_score=50),
        evidence={
            "outcome_status": "not_confirmed",
            "observed_outcome": "Later aggregate evidence did not confirm a real demand shift.",
            "accuracy_score": 20,
        },
        path=path,
    )
    assert weak["outcome_learning_status"] == "historically_weak"
    assert weak["confidence_score"] < 50
    future = apply_outcome_learning(_signal("brief vague signal", confidence_score=50), path=path)
    assert future["outcome_learning_status"] == "historically_weak"
    assert future["confidence_score"] < 50


def test_follow_up_windows_are_recognized():
    assert recognized_follow_up_windows() == [7, 30, 90, 365]


def test_malformed_outcome_memory_recovers_safely(tmp_path):
    path = tmp_path / "outcome_learning_memory.json"
    path.write_text("{bad json", encoding="utf-8")
    memory = load_outcome_memory(path)
    assert memory["clusters"] == {}
    updated = apply_outcome_learning(_signal("jobs in Nairobi"), path=path)
    assert updated["outcome_learning_status"] in {"new", "monitoring", "historically_confirmed", "historically_weak"}


def test_public_ui_remains_privacy_safe_with_outcome_learning(tmp_path):
    signal = apply_outcome_learning(
        _signal("maize flour prices", user_id="private", email="hidden@example.com"),
        evidence={"outcome_status": "confirmed", "accuracy_score": 88, "phone": "private"},
        path=tmp_path / "outcome_learning_memory.json",
    )
    rendered = render_strategic_interpretation([signal])
    lowered = rendered.lower()
    assert "outcome learning" in lowered
    assert "historically" in lowered or "monitored" in lowered
    for forbidden in ["user_id", "hidden@example.com", "phone", "private message", "individual profile"]:
        assert forbidden not in lowered


def test_app_import_and_signal_cge_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source