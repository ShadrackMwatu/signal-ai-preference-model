"""X public trends source placeholder using bearer-token configuration."""

from __future__ import annotations

import os


def is_available() -> bool:
    return bool(os.getenv("X_BEARER_TOKEN"))


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []