from pathlib import Path

import pytest

from Behavioral_Signals_AI.mobility_intelligence.google_places_activity_connector import build_place_activity_profile
from Behavioral_Signals_AI.mobility_intelligence.mobility_signal_scorer import score_place_activity_signal
from Behavioral_Signals_AI.mobility_intelligence.place_activity_cache import read_place_activity_cache, write_place_activity_cache
from Behavioral_Signals_AI.mobility_intelligence.place_classifier import classify_place
from Behavioral_Signals_AI.mobility_intelligence.popularity_signal_engine import generate_place_activity_signal
from Behavioral_Signals_AI.mobility_intelligence.privacy_guard import apply_privacy_guard
from Behavioral_Signals_AI.mobility_intelligence.signal_fusion import fuse_mobility_with_live_signals


def _record(**extra):
    payload = {
        "region": "Kenya",
        "county": "Nairobi",
        "place_name": "Nairobi Supermarket",
        "place_id": "public-place-id",
        "place_category": "food_household_demand",
        "demand_category": "food and agriculture",
        "rating": 4.5,
        "review_count": 760,
        "opening_hours_status": "open_now",
        "business_status": "OPERATIONAL",
        "popularity_level": "high",
        "activity_indicator": "increasing",
        "review_activity_level": "high",
        "estimated_activity_trend": "rising",
        "place_prominence": 82,
        "date": "2026-05-16",
        "source": "google_maps_ecosystem_public_place_metadata",
        "confidence": 84,
    }
    payload.update(extra)
    return payload


def test_forbidden_fields_rejected():
    with pytest.raises(ValueError):
        apply_privacy_guard({"place_name": "Unsafe", "device_id": "abc"})
    safe = apply_privacy_guard(_record())
    assert safe["privacy_status"] == "approved"


def test_place_classification_works():
    assert classify_place("Green Grocery", "supermarket grocery") == "food_household_demand"
    assert classify_place("County Hospital", "clinic hospital") == "health_demand"
    assert classify_place("Main Bus Station", "bus station") == "transport_demand"


def test_google_place_enrichment_without_key_is_safe(monkeypatch):
    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    assert build_place_activity_profile("Kenya") == []
    assert build_place_activity_profile(location_scope="Nairobi") == []


def test_popularity_signal_and_scoring_generate_interpretable_outputs():
    signal = generate_place_activity_signal(apply_privacy_guard(_record()))
    score = score_place_activity_signal(_record())
    assert signal["demand_relevance"] > 0
    assert signal["privacy_level"] == "aggregated_place_intelligence_only"
    assert score["mobility_signal_strength"] > 0


def test_signal_fusion_strengthens_matching_live_signal():
    live = [{"signal_topic": "maize flour prices", "signal_category": "food and agriculture", "confidence_score": 60, "priority_score": 60, "behavioral_intelligence_score": 60}]
    mobility = [generate_place_activity_signal(_record())]
    fused = fuse_mobility_with_live_signals(live, mobility)
    assert fused[0]["confidence_score"] > 60
    assert fused[0]["place_activity_reinforced"] is True
    assert "aggregated" in fused[0]["source_summary"].lower()


def test_place_activity_cache_roundtrip(tmp_path):
    path = tmp_path / "place_cache.json"
    write_place_activity_cache({"records": [_record()], "signals": []}, path=path)
    payload = read_place_activity_cache(path)
    assert "place_name" not in payload["records"][0]
    assert payload["records"][0]["place_id"] == "public-place-id"
    assert payload["records"][0]["review_count"] == 760
    assert payload["privacy_level"] == "aggregated_place_intelligence_only"


def test_no_personal_data_terms_in_mobility_modules():
    root = Path("Behavioral_Signals_AI/mobility_intelligence")
    assert not (root / "demo_mobility_feed.py").exists()
    assert not (root / "footfall_ingestor.py").exists()


def test_app_import_and_signal_cge_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert 'with gr.Tab("Signal CGE")' in source

def test_safe_schema_fields_include_public_place_metadata_only():
    from Behavioral_Signals_AI.mobility_intelligence.mobility_schema import AggregatedPlaceActivityIndicator

    record = AggregatedPlaceActivityIndicator(
        region="Kenya",
        county="Nairobi",
        place_name="Nairobi Supermarket",
        place_id="public-place-id",
        place_category="food_household_demand",
        demand_category="food and agriculture",
        rating=4.5,
        review_count=760,
        opening_hours_status="open_now",
        business_status="OPERATIONAL",
        place_prominence=82,
        popularity_level="high",
        activity_indicator="increasing",
        estimated_activity_trend="rising",
        source="google_maps_ecosystem_public_place_metadata",
        confidence=84,
    ).to_dict()
    forbidden = {"user_id", "device_id", "phone", "gps_trace", "route", "home_location", "work_location", "personal_movement_history"}
    assert not forbidden & set(record)
    assert record["review_count"] == 760
    assert record["business_status"] == "OPERATIONAL"