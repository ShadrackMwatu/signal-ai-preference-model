"""YouTube trend source placeholder for future aggregate API integration."""

from __future__ import annotations

import os


def is_available() -> bool:
    return bool(os.getenv("YOUTUBE_API_KEY"))


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []