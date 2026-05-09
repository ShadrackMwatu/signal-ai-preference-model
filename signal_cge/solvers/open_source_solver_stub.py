"""Placeholder for a future open-source equilibrium solver pathway."""

from __future__ import annotations

from typing import Any


def solve_equilibrium_stub(model_data: dict[str, Any]) -> dict[str, Any]:
    """Return an explicit placeholder response for future solver integration."""

    return {
        "success": False,
        "status": "placeholder",
        "message": "Open-source full CGE equilibrium solving is not implemented yet.",
        "model_data_keys": sorted(model_data.keys()),
    }
