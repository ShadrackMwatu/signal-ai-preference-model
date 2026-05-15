"""KNBS official statistics connector placeholder.

The module is intentionally fail-soft: future official API or curated CSV support can be
added without affecting Hugging Face startup.
"""

from __future__ import annotations

from typing import Any


def collect(location: str = "Kenya", limit: int = 8) -> list[dict[str, Any]]:
    return []