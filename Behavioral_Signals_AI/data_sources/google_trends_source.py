"""Google Trends source placeholder using environment configuration only."""

from __future__ import annotations

import os


def is_available() -> bool:
    return os.getenv("GOOGLE_TRENDS_ENABLED", "").lower() in {"1", "true", "yes"}


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []