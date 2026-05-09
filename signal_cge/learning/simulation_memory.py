"""Runtime simulation learning memory for Signal CGE."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any
import uuid


MEMORY_PATH = Path("outputs") / "signal_cge_learning" / "simulation_memory.jsonl"


def record_simulation_learning_event(event: dict[str, Any], path: str | Path = MEMORY_PATH) -> dict[str, Any]:
    """Persist lightweight simulation metadata without storing uploaded data."""

    memory_path = Path(path)
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    scenario = event.get("scenario", {})
    normalized = {
        "event_id": event.get("event_id") or uuid.uuid4().hex,
        "timestamp": datetime.now(UTC).isoformat(),
        "prompt": str(event.get("prompt", ""))[:500],
        "parsed_scenario": scenario,
        "scenario_type": scenario.get("shock_type") or scenario.get("simulation_type"),
        "target_account": scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account"),
        "shock_type": scenario.get("shock_type"),
        "shock_magnitude": scenario.get("shock_size") or scenario.get("shock_value"),
        "backend_used": event.get("backend_used"),
        "readiness_status": event.get("readiness_status", {}),
        "diagnostics_summary": event.get("diagnostics_summary", {}),
        "result_summary": event.get("result_summary", {}),
        "interpretation_summary": event.get("interpretation_summary", {}),
        "caveats": event.get("caveats", []),
        "recommended_next_simulations": event.get("recommended_next_simulations", []),
        "knowledge_references_used": event.get("knowledge_references_used", []),
    }
    with memory_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(normalized, sort_keys=True) + "\n")
    return normalized


def load_simulation_memory(limit: int = 50, path: str | Path = MEMORY_PATH) -> list[dict[str, Any]]:
    """Load recent learning events."""

    memory_path = Path(path)
    if not memory_path.exists():
        return []
    lines = memory_path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines if line.strip()]
    return events[-limit:]
