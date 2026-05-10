"""Canonical solver registry for Signal CGE backends."""

from __future__ import annotations

from typing import Any

from .gams_runner import get_gams_status


def get_solver_registry() -> dict[str, Any]:
    """Return solver backend availability without requiring optional runtimes."""

    return {
        "validated_static_equilibrium_solver": {
            "status": "ready",
            "required_runtime": "Python/SciPy",
        },
        "static_equilibrium_cge_solver": {
            "status": "ready",
            "required_runtime": "Python/SciPy",
        },
        "open_source_equilibrium_solver": {
            "status": "ready",
            "required_runtime": "Python/SciPy",
        },
        "python_sam_multiplier": {
            "status": "ready",
            "required_runtime": "Python/NumPy",
        },
        "gams_optional_solver": get_gams_status(),
    }


def available_solver_names() -> list[str]:
    return sorted(get_solver_registry())
