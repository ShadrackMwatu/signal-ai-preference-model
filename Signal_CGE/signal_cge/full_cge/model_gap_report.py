"""Report current gaps between Signal CGE prototype and full equilibrium solving."""

from __future__ import annotations

from typing import Any

from .closure_manager import get_closure_options
from .equation_registry import get_equation_registry
from .parameter_registry import get_parameter_registry
from .solver_blueprint import get_solver_blueprint


def generate_full_cge_gap_report() -> dict[str, Any]:
    equations = get_equation_registry()
    parameters = get_parameter_registry()
    return {
        "already_implemented": [
            "SAM multiplier fallback",
            "SAM account classification",
            "prototype share-parameter calibration",
            "equation and variable registries",
            "closure option registry",
            "prompt-to-scenario pathway",
            "knowledge-aware reporting",
        ],
        "still_prototype": [
            "Nonlinear equation forms",
            "elasticity calibration",
            "base-year replication",
            "Walras and homogeneity checks",
            "recursive dynamic solving",
        ],
        "missing_for_full_cge_solving": [
            "Numerical nonlinear solver backend",
            "complete tax-rate calibration",
            "Armington and transformation elasticities",
            "factor-market closure data",
            "government and external closure replacement variables",
        ],
        "next_code_modules_needed": get_solver_blueprint()["required_steps"],
        "missing_data_calibration_requirements": parameters["required_for_full_solve"],
        "registry_status": {
            "equation_blocks": equations["block_count"],
            "closures": len(get_closure_options()),
            "solver_status": "placeholder",
        },
    }
