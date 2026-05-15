"""YouTube public trends connector placeholder for Kenya aggregate topics."""

from __future__ import annotations

import os
from typing import Any


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    if not os.getenv("YOUTUBE_API_KEY"):
        return []
    return []