"""User-authorized website analytics aggregate source placeholder."""

from __future__ import annotations

import os


def is_available() -> bool:
    return bool(os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID"))


def collect(location: str = "Kenya", limit: int = 6) -> list[dict]:
    return []