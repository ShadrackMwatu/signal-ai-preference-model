"""Local JSON simulation history for Signal AI."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any


HISTORY_PATH = Path("cge_workbench/outputs/simulation_history.json")


def save_simulation(record: dict[str, Any]) -> dict[str, Any]:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = _read_history()
    stored = {"timestamp": datetime.now().isoformat(timespec="seconds"), **record}
    history.append(stored)
    HISTORY_PATH.write_text(json.dumps(history[-100:], indent=2), encoding="utf-8")
    return stored


def list_recent_simulations(limit: int = 5) -> list[dict[str, Any]]:
    return list(reversed(_read_history()[-limit:]))


def compare_latest_two() -> dict[str, Any]:
    latest = _read_history()[-2:]
    if len(latest) < 2:
        return {"available": False, "message": "Fewer than two simulations are available."}
    previous, current = latest
    return {
        "available": True,
        "previous_scenario": previous.get("scenario", {}).get("scenario_name"),
        "current_scenario": current.get("scenario", {}).get("scenario_name"),
        "previous_backend": previous.get("backend"),
        "current_backend": current.get("backend"),
    }


def _read_history() -> list[dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return []
    try:
        data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []
