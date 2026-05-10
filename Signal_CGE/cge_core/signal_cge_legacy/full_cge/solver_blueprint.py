"""Open-source solver blueprint for future Signal CGE equilibrium solving."""

from __future__ import annotations

from typing import Any


def get_solver_blueprint() -> dict[str, Any]:
    return {
        "status": "placeholder",
        "current_backend": "SAM multiplier/prototype calibration",
        "future_backend": "open-source nonlinear equation solver",
        "required_steps": [
            "Finalize nonlinear equations.",
            "Complete elasticity and tax-rate calibration.",
            "Implement equation residual functions.",
            "Add numerical solve and convergence diagnostics.",
            "Run base-year replication before policy shocks.",
        ],
    }
