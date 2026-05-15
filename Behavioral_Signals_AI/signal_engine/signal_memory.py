"""Lightweight topical signal memory helpers."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_MEMORY_PATH = Path(os.getenv("SIGNAL_TOPICAL_SIGNAL_MEMORY", "Behavioral_Signals_AI/outputs/topical_signals.json"))


def load_signal_memory(path: str | Path | None = None) -> list[dict[str, Any]]:
    memory_path = Path(path or DEFAULT_MEMORY_PATH)
    if not memory_path.exists():
        return []
    try:
        data = json.loads(memory_path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_signal_memory(signals: list[dict[str, Any]], path: str | Path | None = None) -> None:
    memory_path = Path(path or DEFAULT_MEMORY_PATH)
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    memory_path.write_text(json.dumps(signals, indent=2, ensure_ascii=True), encoding="utf-8")