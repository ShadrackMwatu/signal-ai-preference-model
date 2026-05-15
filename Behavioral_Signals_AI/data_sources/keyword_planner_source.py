"""Keyword-planner style aggregate source placeholder."""

from __future__ import annotations

import os


def is_available() -> bool:
    return bool(os.getenv("GOOGLE_TRENDS_ENABLED") or os.getenv("SERPAPI_API_KEY"))


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []