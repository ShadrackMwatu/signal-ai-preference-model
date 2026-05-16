"""Tiny scheduler helpers for Open Signals runtime loops."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any


def should_run_cycle(last_run_iso: str | None, interval_seconds: int, now: datetime | None = None) -> bool:
    if not last_run_iso:
        return True
    now = now or datetime.now(UTC)
    try:
        last_run = datetime.fromisoformat(str(last_run_iso).replace("Z", "+00:00"))
    except ValueError:
        return True
    if last_run.tzinfo is None:
        last_run = last_run.replace(tzinfo=UTC)
    return now - last_run >= timedelta(seconds=max(1, int(interval_seconds)))


def next_run_hint(last_run_iso: str | None, interval_seconds: int) -> dict[str, Any]:
    return {"should_run": should_run_cycle(last_run_iso, interval_seconds), "interval_seconds": interval_seconds}
