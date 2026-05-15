"""County-aware geospatial filtering tests for Behavioral Signals AI."""

from __future__ import annotations

import json

import pytest

from Behavioral_Signals_AI.geography.county_matcher import (
    county_dropdown_choices,
    detect_county_from_text,
    load_county_registry,
    signal_matches_location,
)
from Behavioral_Signals_AI.mobility_intelligence.privacy_guard import apply_privacy_guard
from Behavioral_Signals_AI.signal_engine import kenya_ui
from Behavioral_Signals_AI.signal_engine.geospatial_learning import load_geospatial_memory, update_geospatial_learning
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache


def test_location_dropdown_includes_global_kenya_and_all_47_counties() -> None:
    choices = county_dropdown_choices()

    assert choices[:2] == ["Global", "Kenya"]
    assert len(choices) == 49
    assert "Mombasa" in choices
    assert "Makueni" in choices
    assert "Uasin Gishu" in choices
    assert "Nairobi" in choices


def test_county_registry_uses_official_codes() -> None:
    registry = load_county_registry()

    assert len(registry) == 47
    assert registry["001"] == "Mombasa"
    assert registry["017"] == "Makueni"
    assert registry["047"] == "Nairobi"


def test_county_alias_detection_for_wote_westlands_and_eldoret() -> None:
    assert detect_county_from_text("Wote market activity is rising")["county_name"] == "Makueni"
    assert detect_county_from_text("Westlands retail demand pressure")["county_name"] == "Nairobi"
    assert detect_county_from_text("Eldoret job searches")["county_name"] == "Uasin Gishu"


def test_unknown_place_defaults_safely_to_kenya_wide() -> None:
    detected = detect_county_from_text("unknown aggregate demand topic")

    assert detected["county_name"] == "Kenya-wide"
    assert detected["county_code"] == ""
    assert detected["geographic_scope"] == "Kenya-wide"


def test_signal_matches_specific_county() -> None:
    wote_signal = {"signal_topic": "Wote maize flour price pressure", "geographic_scope": "Makueni"}
    westlands_signal = {"signal_topic": "Westlands restaurant demand", "geographic_scope": "Nairobi"}

    assert signal_matches_location(wote_signal, "Makueni")
    assert not signal_matches_location(westlands_signal, "Makueni")


def test_county_filter_changes_feed_content_and_falls_back_to_kenya_wide(tmp_path, monkeypatch) -> None:
    signal_cache = tmp_path / "latest_live_signals.json"
    render_cache = tmp_path / "render_cache.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(signal_cache))
    monkeypatch.setenv("SIGNAL_RENDER_CACHE", str(render_cache))

    payload = {
        "last_updated": "2026-05-16T00:00:00+03:00",
        "status": "test",
        "privacy_level": "aggregate_public",
        "signals": [
            _signal("Wote maize flour prices", "Makueni", "017", 82),
            _signal("Westlands retail traffic", "Nairobi", "047", 78),
            _signal("Kenya food affordability pressure", "Kenya-wide", "", 60),
        ],
    }
    write_signal_cache(payload, signal_cache)
    kenya_ui.reset_live_feed_render_cache()

    makueni_feed, makueni_emerging, makueni_interpretation, _ = kenya_ui.get_kenya_live_signals_for_ui("Makueni", "All", "All")
    assert "Wote maize flour prices" in makueni_feed
    assert "Westlands retail traffic" not in makueni_feed
    assert "Makueni" in makueni_emerging or "Makueni" in makueni_interpretation

    kisumu_feed, _, _, _ = kenya_ui.get_kenya_live_signals_for_ui("Kisumu", "All", "All")
    assert "Kenya food affordability pressure" in kisumu_feed
    assert "Westlands retail traffic" not in kisumu_feed


def test_geospatial_memory_initializes_and_updates_aggregate_fields(tmp_path) -> None:
    memory_path = tmp_path / "geospatial_signal_memory.json"

    memory = load_geospatial_memory(memory_path)
    assert memory["clusters"] == {}
    updated = update_geospatial_learning(_signal("Wote maize flour prices", "Makueni", "017", 74), memory_path)
    stored = load_geospatial_memory(memory_path)

    assert updated["county_name"] == "Makueni"
    assert updated["county_code"] == "017"
    assert stored["privacy_level"] == "county_level_aggregate_only"
    assert stored["clusters"]
    cluster = next(iter(stored["clusters"].values()))
    assert set(cluster).issuperset({"county_code", "county_name", "signal_cluster", "appearance_count", "category_history", "urgency_history", "learned_pattern"})


def test_privacy_guard_blocks_exact_personal_location_fields() -> None:
    with pytest.raises(ValueError):
        apply_privacy_guard({"place_name": "Private movement record", "personal_location": "exact home coordinate"})


def _signal(topic: str, scope: str, code: str, score: float) -> dict[str, object]:
    county_name = scope if scope != "Kenya-wide" else "Kenya-wide"
    return {
        "signal_topic": topic,
        "signal_category": "food and agriculture" if "maize" in topic.lower() or "food" in topic.lower() else "trade and business",
        "demand_level": "High",
        "opportunity_level": "Moderate",
        "unmet_demand_likelihood": "Medium",
        "urgency": "High" if score >= 80 else "Medium",
        "geographic_scope": scope,
        "county_name": county_name,
        "county_code": code,
        "source_summary": "Aggregate public sources",
        "confidence_score": score,
        "priority_score": score,
        "behavioral_intelligence_score": score,
        "momentum": "Rising",
        "forecast_direction": "Rising",
        "spread_risk": "Moderate" if scope != "Kenya-wide" else "Low",
        "geospatial_insight": f"{scope} aggregate evidence is being monitored.",
        "last_updated": "2026-05-16T00:00:00+03:00",
        "recommended_action": "Monitor aggregate county-level evidence.",
        "privacy_level": "aggregate_public",
    }
