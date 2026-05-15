"""Reddit public Kenya connector placeholder using configured API credentials only."""

from __future__ import annotations

import os
from typing import Any


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    if not (os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET")):
        return []
    return []