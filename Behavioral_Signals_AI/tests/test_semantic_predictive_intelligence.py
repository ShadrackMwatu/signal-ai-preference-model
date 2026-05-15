from pathlib import Path

from Behavioral_Signals_AI.signal_engine.early_warning_engine import classify_early_warning
from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals
from Behavioral_Signals_AI.signal_engine.predictive_signal_engine import estimate_county_spread_risk, predict_signal_evolution
from Behavioral_Signals_AI.signal_engine.semantic_intelligence import canonical_theme, cluster_related_topics
from Behavioral_Signals_AI.signal_engine.signal_relationships import detect_signal_relationships
from Behavioral_Signals_AI.signal_engine.source_learning import update_source_learning


def test_semantic_clustering_merges_synonymous_demand_topics():
    signals = [
        {"signal_topic": "cheap smartphones Kenya", "confidence_score": 70},
        {"signal_topic": "budget android phones", "confidence_score": 65},
        {"signal_topic": "affordable smartphones Kenya", "confidence_score": 80},
    ]
    clusters = cluster_related_topics(signals)
    assert canonical_theme("cheap smartphones Kenya") == "Affordable smartphone demand"
    assert any(cluster["semantic_cluster"] == "Affordable smartphone demand" and len(cluster["signals"]) >= 2 for cluster in clusters)


def test_relationship_detection_links_pressure_chain():
    graph = detect_signal_relationships(
        [
            {"signal_topic": "fuel prices", "signal_category": "energy", "geographic_scope": "Kenya-wide"},
            {"signal_topic": "transport costs", "signal_category": "transport", "geographic_scope": "Kenya-wide"},
            {"signal_topic": "food prices Kenya", "signal_category": "food and agriculture", "geographic_scope": "Kenya-wide"},
        ]
    )
    descriptions = " ".join(edge["description"] for edge in graph["edges"])
    assert "transport" in descriptions
    assert "food" in descriptions


def test_predictive_direction_and_county_spread_assignment():
    signal = {
        "signal_topic": "maize flour prices",
        "signal_category": "food and agriculture",
        "momentum": "Rising",
        "urgency": "High",
        "confidence_score": 76,
        "multi_source_confirmation_score": 80,
        "geographic_scope": "Kenya-wide",
    }
    prediction = predict_signal_evolution(signal, {"clusters": {}}, [])
    assert prediction["predicted_direction"] == "rising"
    assert prediction["spread_risk"] == "High"
    assert estimate_county_spread_risk(signal) == "High"


def test_early_warning_classification_and_confidence_reasoning():
    warning = classify_early_warning(
        {
            "signal_topic": "water shortage",
            "signal_category": "water and sanitation",
            "momentum": "Breakout",
            "urgency": "High",
            "confidence_score": 78,
            "priority_score": 84,
            "multi_source_confirmation_score": 72,
        },
        [],
    )
    assert "Early warning" in warning["early_warning_labels"]
    fused = fuse_kenya_signals(limit=3)
    assert fused
    assert all(signal.get("confidence_reasoning") for signal in fused)
    assert all(signal.get("predicted_direction") in {"rising", "stable", "declining"} for signal in fused)


def test_source_learning_updates_without_personal_fields(tmp_path):
    target = tmp_path / "source_learning.json"
    payload = update_source_learning(
        [
            {
                "signal_topic": "Affordable smartphone demand",
                "semantic_cluster": "Affordable smartphone demand",
                "source_summary": "Search Trends + Public News",
                "accuracy_confidence": 70,
                "geographic_scope": "Kenya-wide",
                "predicted_direction": "rising",
                "signal_category": "technology and digital economy",
            }
        ],
        path=target,
    )
    assert target.exists()
    serialized = target.read_text(encoding="utf-8").lower()
    assert "search trends" in serialized
    assert "user_id" not in serialized
    assert "email" not in serialized
    assert payload["last_updated"]


def test_app_import_and_signal_cge_tab_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source
