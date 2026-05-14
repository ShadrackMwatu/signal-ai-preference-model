from __future__ import annotations

import os
from unittest.mock import patch

from Behavioral_Signals_AI.providers.provider_base import assert_privacy_safe_signals, normalize_signal
from Behavioral_Signals_AI.providers.provider_registry import build_provider_registry
from Behavioral_Signals_AI.providers.provider_router import fetch_aggregate_signals, rank_and_deduplicate_signals
from Behavioral_Signals_AI.live_trends.trend_router import fetch_live_trends


def test_provider_registry_contains_phase_one_and_future_providers():
    registry = build_provider_registry()

    for key in ["google", "serpapi", "pytrends", "x", "gdelt", "news", "tiktok", "youtube", "jumia", "maps", "fintech", "appstore"]:
        assert key in registry


def test_provider_router_falls_back_without_credentials():
    env = {
        "SIGNAL_TRENDS_MODE": "auto",
        "GOOGLE_TRENDS_API_KEY": "",
        "SERPAPI_API_KEY": "",
        "X_BEARER_TOKEN": "",
        "NEWS_API_KEY": "",
        "SIGNAL_ENABLE_GDELT": "",
    }
    with patch.dict(os.environ, env, clear=False):
        result = fetch_aggregate_signals("Kenya", 4)

    assert result.mode_badge == "Demo fallback"
    assert result.signals
    assert all(signal["privacy_level"] == "aggregate_public" for signal in result.signals)


def test_schema_normalization_and_privacy_safe_output():
    signal = normalize_signal({"query": "maize flour prices", "traffic": "12K"}, source="Google Trends", provider_type="search")

    assert signal["signal_name"] == "maize flour prices"
    assert signal["provider_type"] == "search"
    assert signal["category"] == "prices" or signal["category"] == "food_agriculture"
    assert signal["privacy_level"] == "aggregate_public"
    assert assert_privacy_safe_signals([signal]) == [signal]


def test_deduplication_keeps_stronger_overlapping_topic():
    signals = [
        normalize_signal({"signal_name": "fuel prices", "volume": 1000, "confidence": 0.4}, source="A", provider_type="search"),
        normalize_signal({"signal_name": "fuel prices", "volume": 200000, "confidence": 0.9}, source="B", provider_type="social"),
    ]

    ranked = rank_and_deduplicate_signals(signals)
    assert len(ranked) == 1
    assert ranked[0]["source"] == "B"


def test_live_trend_dashboard_adapter_uses_provider_router():
    with patch.dict(os.environ, {"SIGNAL_TRENDS_MODE": "demo"}, clear=False):
        result = fetch_live_trends("Kenya", 3)

    assert result.source_label == "Demo fallback"
    assert result.records
    assert result.records[0]["mode_badge"] == "Demo fallback"
    assert result.records[0]["privacy_level"] == "aggregate_public"


def test_live_mode_with_configured_provider_can_be_mocked():
    class FakeProvider:
        provider_name = "fake_google"
        provider_type = "search"
        source_label = "Google Trends"

        def is_available(self):
            return True

        def fetch_signals(self, location="Kenya", limit=10):
            from Behavioral_Signals_AI.providers.provider_base import ProviderResult, ProviderStatus, normalize_signals

            signals = normalize_signals([{"signal_name": "jobs in Nairobi", "source": "Google Trends", "volume": 100000}], source="Google Trends", provider_type="search", location=location)
            return ProviderResult(signals, self.provider_name, self.provider_type, self.source_label, True, ProviderStatus(self.provider_name, self.provider_type, True, True, "google", "ok"))

    with patch("Behavioral_Signals_AI.providers.provider_router.build_provider_registry", return_value={"google": FakeProvider()}), patch("Behavioral_Signals_AI.providers.provider_router.phase_one_provider_keys", return_value=["google"]):
        result = fetch_aggregate_signals("Kenya", 2)

    assert result.mode_badge == "Live Kenya signals"
    assert result.source_label == "Google Trends"
    assert result.signals[0]["provider_type"] == "search"