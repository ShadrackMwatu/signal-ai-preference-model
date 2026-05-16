from __future__ import annotations

import os
from unittest.mock import patch

import pandas as pd

from Behavioral_Signals_AI.live_trends.fallback_demo_provider import get_demo_trends
from Behavioral_Signals_AI.live_trends.trend_normalizer import assert_aggregate_privacy, normalize_trend_record
from Behavioral_Signals_AI.live_trends.trend_router import fetch_live_trends, get_trend_provider_status


def test_fallback_provider_without_credentials_returns_standard_records():
    with patch.dict(os.environ, {"SIGNAL_TRENDS_MODE": "auto", "X_BEARER_TOKEN": "", "SERPAPI_API_KEY": "", "GOOGLE_TRENDS_API_KEY": "", "APIFY_API_TOKEN": ""}, clear=False):
        result = fetch_live_trends(location="Kenya", limit=3)

    assert result.source_label == "Fallback aggregate intelligence"
    assert result.records
    assert len(result.records) == 3
    record = result.records[0]
    for field in [
        "trend_name",
        "platform",
        "location",
        "volume",
        "growth_indicator",
        "category",
        "timestamp",
        "confidence",
        "relevance_to_demand",
        "possible_policy_or_business_implication",
    ]:
        assert field in record


def test_trend_normalization_classifies_demand_context():
    record = normalize_trend_record({"name": "Fuel prices", "traffic": "12K"}, platform="Google Trends", location="Kenya", rank=1)

    assert record["trend_name"] == "Fuel prices"
    assert record["volume"] == 12000
    assert record["category"] == "prices"
    assert "price" in record["possible_policy_or_business_implication"].lower()


def test_privacy_compliance_rejects_personal_fields():
    try:
        assert_aggregate_privacy([{"trend_name": "Topic", "username": "person"}])
    except ValueError as exc:
        assert "aggregate only" in str(exc)
    else:
        raise AssertionError("personal fields should be rejected")


def test_dashboard_live_trend_output_shape():
    from app import build_live_trend_html, refresh_live_trend_intelligence, refresh_live_trends

    with patch.dict(os.environ, {"SIGNAL_TRENDS_MODE": "demo"}, clear=False):
        trends_frame, intelligence_frame, summary = refresh_live_trends("Kenya", 4)
        display_table, html, active_count, panel, _, demand_signals = refresh_live_trend_intelligence("Kenya", 4)

    assert isinstance(trends_frame, pd.DataFrame)
    assert not trends_frame.empty
    assert not intelligence_frame.empty
    assert "Source:" in summary
    assert "What these Kenya trends may imply" in panel
    assert active_count == 4
    assert not demand_signals.empty
    for column in ["trend_name", "inferred_demand_category", "demand_signal_strength", "possible_unmet_demand", "urgency", "recommendation", "confidence_score"]:
        assert column in demand_signals.columns
    for column in ["trend_name", "source", "category", "signal_strength", "demand_relevance", "policy_business_implication", "timestamp"]:
        assert column in display_table.columns
    html = build_live_trend_html(trends_frame)
    assert "Live Trend Intelligence" in html
    assert "active trends" in html
    assert "Fallback aggregate intelligence" in html
    assert "Signal Strength" in html
    assert "Demand Relevance" in html


def test_provider_status_does_not_expose_secrets():
    with patch.dict(os.environ, {"X_BEARER_TOKEN": "secret-token", "SIGNAL_TRENDS_MODE": "auto"}, clear=False):
        status = get_trend_provider_status()

    assert status["x_available"] is True
    assert "secret-token" not in str(status)


def test_demo_provider_records_are_aggregate_only():
    records = get_demo_trends("Kenya", limit=2)
    assert records
    forbidden = {"username", "user_id", "profile_url", "text"}
    assert all(not forbidden.intersection(record) for record in records)