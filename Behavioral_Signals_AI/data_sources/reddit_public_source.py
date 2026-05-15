"""Reddit public aggregate source placeholder for configured API access."""

from __future__ import annotations

import os


def is_available() -> bool:
    return bool(os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET"))


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []