"""Runtime heartbeat state for Open Signals."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

HEARTBEAT_PATH = Path("Behavioral_Signals_AI/outputs/runtime_heartbeat.json")


def write_runtime_heartbeat(status: str, details: dict[str, Any] | None = None, path: str | Path | None = None) -> dict[str, Any]:
    payload = {
        "status": status,
        "last_heartbeat": datetime.now(UTC).isoformat(),
        "details": details or {},
        "privacy_level": "aggregate_public",
    }
    write_json(path or HEARTBEAT_PATH, payload)
    return payload


def read_runtime_heartbeat(path: str | Path | None = None) -> dict[str, Any]:
    return read_json(path or HEARTBEAT_PATH, {"status": "missing", "details": {}, "privacy_level": "aggregate_public"})
