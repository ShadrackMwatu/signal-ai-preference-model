"""Signal persistence model using repeated aggregate appearances and growth."""

from __future__ import annotations

from typing import Any


def estimate_signal_persistence(signal: dict[str, Any], history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    history = history or []
    key = _key(signal.get("signal_name") or signal.get("trend_name"))
    repeats = sum(1 for row in history if _key(row.get("signal_name") or row.get("trend_name")) == key)
    growth = str(signal.get("growth") or signal.get("growth_indicator") or "").lower()
    base = 42 + repeats * 12
    if "rising" in growth or "breakout" in growth:
        base += 18
    if "declin" in growth or "down" in growth:
        base -= 18
    score = min(max(base, 5), 98)
    return {"signal_persistence_score": round(score, 2), "persistence_label": "Persistent" if score >= 70 else "Watch" if score >= 45 else "Short-lived"}


def _key(value: Any) -> str:
    return " ".join(str(value or "").lower().split()[:4])