"""Lightweight topical signal memory helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

DEFAULT_MEMORY_PATH = Path(os.getenv("SIGNAL_TOPICAL_SIGNAL_MEMORY", "Behavioral_Signals_AI/outputs/topical_signals.json"))


def load_signal_memory(path: str | Path | None = None) -> list[dict[str, Any]]:
    data = read_json(Path(path or DEFAULT_MEMORY_PATH), [])
    return data if isinstance(data, list) else []


def save_signal_memory(signals: list[dict[str, Any]], path: str | Path | None = None) -> None:
    write_json(Path(path or DEFAULT_MEMORY_PATH), signals)
