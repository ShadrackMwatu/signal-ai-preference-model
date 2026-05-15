"""Durable JSON storage manager for Behavioral Signals AI learning memory."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LAST_SUCCESSFUL_WRITE: str | None = None
LAST_STORAGE_WARNING: str | None = None


def read_json(path: str | Path, default: Any) -> Any:
    """Read JSON safely, recovering to default if the file is missing or malformed."""
    target = Path(path)
    if not target.exists():
        return default
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
        return default if data is None or data == "" else data
    except Exception as exc:
        _mark_warning(f"Recovered malformed JSON at {target}: {exc}")
        _preserve_corrupt_copy(target)
        return default


def write_json(path: str | Path, payload: Any, *, backup: bool = True) -> dict[str, Any]:
    """Write JSON atomically with an optional backup of the previous version."""
    global LAST_SUCCESSFUL_WRITE
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if backup and target.exists():
        _backup_existing(target)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=True)
        Path(tmp_name).replace(target)
        LAST_SUCCESSFUL_WRITE = datetime.now(UTC).isoformat()
        return {"ok": True, "path": str(target), "last_successful_write": LAST_SUCCESSFUL_WRITE}
    except Exception as exc:
        _mark_warning(f"Atomic write failed for {target}: {exc}")
        try:
            Path(tmp_name).unlink(missing_ok=True)
        except Exception:
            pass
        return {"ok": False, "path": str(target), "error": str(exc), "last_successful_write": LAST_SUCCESSFUL_WRITE}


def ensure_json(path: str | Path, default: Any) -> Any:
    target = Path(path)
    if not target.exists():
        write_json(target, default, backup=False)
        return default
    return read_json(target, default)


def storage_health(paths: dict[str, str | Path] | None = None) -> dict[str, Any]:
    checked = {}
    for name, path in (paths or {}).items():
        target = Path(path)
        checked[name] = {
            "available": target.exists(),
            "path": str(target),
            "size_bytes": target.stat().st_size if target.exists() else 0,
        }
    return {
        "memory_available": checked.get("memory", {}).get("available", False),
        "history_available": checked.get("history", {}).get("available", False),
        "forecast_memory_available": checked.get("forecast", {}).get("available", False),
        "last_successful_write": LAST_SUCCESSFUL_WRITE,
        "last_warning": LAST_STORAGE_WARNING,
        "backend": "local_json",
        "future_backends": ["hugging_face_dataset", "hugging_face_repo"],
        "checked_paths": checked,
    }


def _backup_existing(target: Path) -> None:
    backup = target.with_suffix(target.suffix + ".bak")
    try:
        shutil.copy2(target, backup)
    except Exception as exc:
        _mark_warning(f"Could not create backup for {target}: {exc}")


def _preserve_corrupt_copy(target: Path) -> None:
    corrupt = target.with_suffix(target.suffix + f".corrupt-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}")
    try:
        shutil.copy2(target, corrupt)
    except Exception:
        pass


def _mark_warning(message: str) -> None:
    global LAST_STORAGE_WARNING
    LAST_STORAGE_WARNING = message

