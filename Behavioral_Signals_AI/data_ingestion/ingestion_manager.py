"""Manage privacy-preserving ingestion from public/aggregate sources."""

from __future__ import annotations

import importlib
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.data_ingestion.normalizer import normalize_record, validate_normalized_record
from Behavioral_Signals_AI.data_ingestion.privacy_filter import apply_ingestion_privacy_filter
from Behavioral_Signals_AI.data_ingestion.source_registry import load_ingestion_source_registry
from Behavioral_Signals_AI.signal_engine.signal_cache import write_signal_cache
from Behavioral_Signals_AI.storage.storage_manager import write_json

INGESTED_RECORDS_PATH = Path(os.getenv("SIGNAL_INGESTED_RECORDS_PATH", "Behavioral_Signals_AI/outputs/ingested_signal_records.json"))

CONNECTOR_MODULES = {
    "knbs": "Behavioral_Signals_AI.data_sources.knbs_connector",
    "cbk": "Behavioral_Signals_AI.data_sources.cbk_connector",
    "world bank open data": "Behavioral_Signals_AI.data_sources.worldbank_connector",
    "google trends / serpapi": "Behavioral_Signals_AI.data_sources.google_trends_connector",
    "kenya news/public reports": "Behavioral_Signals_AI.data_sources.kenya_news_connector",
    "kilimostat": "Behavioral_Signals_AI.data_sources.kilimostat_connector",
    "aggregate mobility placeholder": "Behavioral_Signals_AI.data_sources.aggregate_mobility_connector",
}


def ingest_enabled_sources(registry_path: str | Path | None = None, output_path: str | Path | None = None, *, include_disabled_samples: bool = True) -> dict[str, Any]:
    """Ingest public/aggregate source records safely.

    Massive data collection principle: collect massive aggregate intelligence, not personal data.
    """
    sources = load_ingestion_source_registry(registry_path)
    records: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    for source in sources:
        status = _source_status(source)
        statuses.append(status)
        if not status["should_collect"] and not include_disabled_samples:
            continue
        try:
            raw_records = _collect_source(source) if status["should_collect"] else _sample_records_for_disabled_source(source)
            for raw in raw_records:
                normalized = normalize_record(raw, source)
                filtered = apply_ingestion_privacy_filter(normalized)
                if filtered and validate_normalized_record(filtered):
                    records.append(filtered)
            status["records_collected"] = len(raw_records)
            status["status"] = "available" if status["should_collect"] else "sample_aggregate"
        except Exception as exc:
            status["status"] = "failed"
            status["warning"] = str(exc)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "privacy_principle": "Collect massive aggregate intelligence, not personal data.",
        "records": records,
        "source_status": statuses,
        "privacy_level": "aggregate",
    }
    write_json(output_path or INGESTED_RECORDS_PATH, payload)
    if records:
        _update_live_signal_cache(records)
    return payload


def connector_status_report(registry_path: str | Path | None = None) -> dict[str, Any]:
    sources = load_ingestion_source_registry(registry_path)
    statuses = [_source_status(source) for source in sources]
    return {"generated_at": datetime.now(UTC).isoformat(), "sources": statuses}


def _source_status(source: dict[str, Any]) -> dict[str, Any]:
    enabled = bool(source.get("enabled"))
    requires_key = bool(source.get("requires_api_key"))
    env_var = str(source.get("env_var") or source.get("environment_key") or "")
    has_credentials = (not requires_key) or bool(env_var and os.getenv(env_var))
    should_collect = enabled and has_credentials
    return {
        "source_name": source.get("source_name") or source.get("name"),
        "source_type": source.get("source_type"),
        "enabled": enabled,
        "requires_api_key": requires_key,
        "env_var": env_var,
        "has_credentials": has_credentials,
        "should_collect": should_collect,
        "status": "available" if should_collect else "missing_credentials" if enabled and requires_key else "disabled",
        "records_collected": 0,
    }


def _collect_source(source: dict[str, Any]) -> list[dict[str, Any]]:
    source_name = str(source.get("source_name") or source.get("name") or "").lower()
    module_name = CONNECTOR_MODULES.get(source_name)
    if not module_name:
        return _sample_records_for_disabled_source(source)
    module = importlib.import_module(module_name)
    return list(module.collect(source))


def _sample_records_for_disabled_source(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "topic": f"{source.get('source_name') or source.get('name')} aggregate readiness signal",
        "category": _category_for_source(source),
        "source_name": source.get("source_name") or source.get("name"),
        "source_type": source.get("source_type"),
        "location": "Kenya" if float(source.get("kenya_relevance_prior", 0) or 0) >= 70 else "Global",
        "relative_interest": min(100, max(20, float(source.get("kenya_relevance_prior", 50) or 50))),
        "confidence": min(100, max(20, float(source.get("reliability_prior", 50) or 50))),
        "summary": "Safe aggregate placeholder for future real API activation; no personal data collected.",
        "raw_reference": str(source.get("source_name") or source.get("name")),
    }]


def _update_live_signal_cache(records: list[dict[str, Any]]) -> None:
    signals = []
    for record in records[:12]:
        score = float(record.get("relative_interest", 50) or 50) * 0.5 + float(record.get("confidence", 50) or 50) * 0.5
        signals.append({
            "signal_topic": record["topic"],
            "signal_category": record["category"],
            "demand_level": "High" if score >= 75 else "Moderate" if score >= 45 else "Low",
            "opportunity_level": "High" if score >= 78 else "Moderate" if score >= 45 else "Low",
            "unmet_demand_likelihood": "High" if score >= 80 else "Medium" if score >= 45 else "Low",
            "urgency": "High" if score >= 82 else "Medium" if score >= 45 else "Low",
            "geographic_scope": record.get("location") or "Kenya",
            "county_name": record.get("county_name") or record.get("location") or "Kenya-wide",
            "source_summary": f"Retrieved from: {record.get('source_name')} ({record.get('source_type')})",
            "confidence_score": round(float(record.get("confidence", score) or score), 1),
            "priority_score": round(score, 2),
            "behavioral_intelligence_score": round(score, 2),
            "momentum": "Rising" if score >= 65 else "Stable",
            "forecast_direction": "Rising" if score >= 70 else "Stable",
            "spread_risk": "Moderate",
            "interpretation": record.get("summary"),
            "recommended_action": "Monitor this aggregate source, validate recurrence, and compare with historical and outcome evidence.",
            "privacy_level": "aggregate_public",
        })
    write_signal_cache({"last_updated": datetime.now(UTC).isoformat(), "status": "ingested_aggregate_records", "signals": signals, "privacy_level": "aggregate_public"})


def _category_for_source(source: dict[str, Any]) -> str:
    source_type = str(source.get("source_type") or "")
    return {
        "macro": "finance",
        "agriculture": "food and agriculture",
        "food_prices": "cost of living",
        "news": "public services",
        "search_trends": "cost of living",
        "social_public": "public services",
        "geospatial": "climate and environment",
        "mobility_aggregate": "trade and business",
    }.get(source_type, "other")
