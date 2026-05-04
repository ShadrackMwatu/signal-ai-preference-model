"""Execution logging helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


def write_log(output_dir: str | Path, message: str) -> str:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "execution.log"
    timestamp = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    return str(path)
