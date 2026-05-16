"""Learning cycle that connects ingestion, retrieval, cache, and metrics for Open Signals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.ai_platform.intelligence_orchestrator import run_open_signals_learning_cycle as run_ai_platform_metrics_cycle
from Behavioral_Signals_AI.data_ingestion.ingestion_manager import ingest_enabled_sources
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

OUTPUTS_DIR = Path("Behavioral_Signals_AI/outputs")


def run_open_signals_learning_cycle(registry_path: str | Path | None = None) -> dict[str, Any]:
    """Run a safe aggregate learning refresh.

    The cycle ingests public/aggregate records, updates cache through the ingestion manager,
    refreshes evaluation metrics, and keeps running if individual sources fail.
    """
    ingestion = ingest_enabled_sources(registry_path)
    _append_lightweight_memory("historical_signal_memory.json", ingestion.get("records", []), "historical")
    _append_lightweight_memory("geospatial_signal_memory.json", ingestion.get("records", []), "geospatial")
    _append_lightweight_memory("outcome_learning_memory.json", ingestion.get("records", []), "outcome_monitoring")
    metrics = run_ai_platform_metrics_cycle()
    return {"ingestion": ingestion, "evaluation_metrics": metrics, "privacy_level": "aggregate_public"}


def _append_lightweight_memory(filename: str, records: list[dict[str, Any]], memory_type: str) -> None:
    path = OUTPUTS_DIR / filename
    existing = read_json(path, [])
    if not isinstance(existing, list):
        existing = []
    additions = []
    for record in records[:10]:
        additions.append({
            "memory_type": memory_type,
            "signal_topic": record.get("topic"),
            "category": record.get("category"),
            "county_or_scope": record.get("county_name") or record.get("location"),
            "confidence_score": record.get("confidence"),
            "lessons_learned": "Aggregate retrieved evidence is available for future validation and recurrence checks.",
            "privacy_level": "aggregate",
        })
    combined = (existing + additions)[-200:]
    write_json(path, combined)
