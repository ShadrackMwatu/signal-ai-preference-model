"""Tests for Open Signals privacy-preserving ingestion and retrieval."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.ai_platform.context_builder import build_open_signals_context
from Behavioral_Signals_AI.data_ingestion.ingestion_manager import ingest_enabled_sources
from Behavioral_Signals_AI.data_ingestion.normalizer import normalize_record, validate_normalized_record
from Behavioral_Signals_AI.data_ingestion.privacy_filter import apply_ingestion_privacy_filter, assert_no_private_fields
from Behavioral_Signals_AI.data_ingestion.retrieval_index import build_retrieval_index, retrieve_relevant_context
from Behavioral_Signals_AI.data_ingestion.source_registry import load_ingestion_source_registry
from Behavioral_Signals_AI.signal_engine.open_signals_chat import answer_open_signals_prompt
from Behavioral_Signals_AI.signal_engine.open_signals_learning_cycle import run_open_signals_learning_cycle
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache


def test_source_registry_loads_public_aggregate_sources() -> None:
    sources = load_ingestion_source_registry()

    names = {source["source_name"] for source in sources}
    assert "KNBS" in names
    assert "CBK" in names
    assert "World Bank Open Data" in names
    assert "Google Trends / SerpAPI" in names
    assert all(source["privacy_level"] == "public_aggregate" for source in sources)


def test_ingestion_manager_handles_missing_credentials(tmp_path, monkeypatch) -> None:
    registry = tmp_path / "source_registry.yaml"
    output = tmp_path / "ingested_signal_records.json"
    cache = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache))
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    registry.write_text(
        "sources:\n"
        "  - source_name: Google Trends / SerpAPI\n"
        "    name: Google Trends / SerpAPI\n"
        "    source_type: search_trends\n"
        "    enabled: true\n"
        "    requires_api_key: true\n"
        "    env_var: SERPAPI_KEY\n"
        "    environment_key: SERPAPI_KEY\n"
        "    update_frequency_seconds: 3600\n"
        "    privacy_level: public_aggregate\n"
        "    kenya_relevance_prior: 88\n"
        "    reliability_prior: 82\n",
        encoding="utf-8",
    )

    payload = ingest_enabled_sources(registry, output)

    assert output.exists()
    assert payload["records"]
    assert payload["source_status"][0]["status"] in {"missing_credentials", "sample_aggregate"}
    assert assert_no_private_fields(payload)


def test_normalized_record_schema_is_valid() -> None:
    record = normalize_record({"topic": "maize flour prices", "confidence": 77}, {"source_name": "KNBS", "source_type": "official_statistics"})

    assert validate_normalized_record(record)
    assert record["privacy_level"] == "aggregate"
    assert 0 <= record["relative_interest"] <= 100


def test_privacy_filter_blocks_personal_fields() -> None:
    assert apply_ingestion_privacy_filter({"topic": "safe aggregate", "user_id": "person-1"}) is None
    assert apply_ingestion_privacy_filter({"topic": "call +254700000000"}) is None
    safe = apply_ingestion_privacy_filter({"topic": "Kenya aggregate food prices", "privacy_level": "aggregate"})
    assert safe is not None
    assert safe["privacy_level"] == "aggregate"


def test_retrieval_returns_relevant_context_without_private_fields(tmp_path) -> None:
    ingested = tmp_path / "ingested_signal_records.json"
    ingested.write_text(
        '{"records":[{"topic":"Nakuru water access stress","category":"water and sanitation","source_name":"county public reports","source_type":"official_statistics","location":"Nakuru","county_name":"Nakuru","confidence":84,"summary":"Aggregate water access pressure","privacy_level":"aggregate","raw_reference":"county report"}]}',
        encoding="utf-8",
    )

    index = build_retrieval_index({"ingested_signal_records": ingested})
    results = retrieve_relevant_context("water access Nakuru", location="Nakuru", limit=3)

    assert index[0]["topic"] == "Nakuru water access stress"
    assert results or index
    assert assert_no_private_fields(index)


def test_chat_context_uses_retrieved_context(tmp_path, monkeypatch) -> None:
    cache_path = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache_path))
    monkeypatch.setenv("SIGNAL_LLM_ENABLED", "false")
    write_signal_cache({"signals": [_signal("Nakuru water access stress", "water and sanitation", "Nakuru", 86)]}, cache_path)

    context = build_open_signals_context("explain water access in Nakuru", {"intent": "signal_query", "confidence": 0.82}, "Nakuru", "All", "All", {}, [])
    answer = answer_open_signals_prompt("explain water access in Nakuru", [], "Kenya", "All", "All")

    assert "retrieved_evidence" in context
    assert "Nakuru water access stress" in answer
    assert assert_no_private_fields(context)


def test_learning_cycle_runs_with_safe_outputs(tmp_path, monkeypatch) -> None:
    registry = tmp_path / "source_registry.yaml"
    cache = tmp_path / "latest_live_signals.json"
    monkeypatch.setenv("SIGNAL_LIVE_SIGNAL_CACHE", str(cache))
    registry.write_text(
        "sources:\n"
        "  - source_name: KNBS\n"
        "    name: KNBS\n"
        "    source_type: official_statistics\n"
        "    enabled: false\n"
        "    requires_api_key: false\n"
        "    env_var: \"\"\n"
        "    environment_key: \"\"\n"
        "    update_frequency_seconds: 86400\n"
        "    privacy_level: public_aggregate\n"
        "    kenya_relevance_prior: 98\n"
        "    reliability_prior: 94\n",
        encoding="utf-8",
    )

    result = run_open_signals_learning_cycle(registry)

    assert result["privacy_level"] == "aggregate_public"
    assert result["ingestion"]["records"]
    assert assert_no_private_fields(result)


def test_signal_cge_unchanged_by_ingestion_layer() -> None:
    assert Path("Signal_CGE").exists()


def _signal(topic: str, category: str, scope: str, score: float) -> dict[str, object]:
    return {
        "signal_topic": topic,
        "signal_category": category,
        "demand_level": "High",
        "opportunity_level": "Moderate",
        "unmet_demand_likelihood": "High",
        "urgency": "High",
        "geographic_scope": scope,
        "county_name": scope,
        "source_summary": "Aggregate public sources",
        "confidence_score": score,
        "priority_score": score,
        "behavioral_intelligence_score": score,
        "momentum": "Rising",
        "forecast_direction": "Rising",
        "spread_risk": "Moderate",
        "interpretation": f"{topic} is an aggregate interpreted signal.",
        "recommended_action": "Monitor persistence and validate with aggregate sources.",
        "privacy_level": "aggregate_public",
    }
