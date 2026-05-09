"""Central registry for Signal CGE model layers and capabilities."""

from __future__ import annotations


def get_model_registry() -> dict[str, object]:
    """Return the canonical Signal CGE registry."""

    return {
        "model_identity": "Signal CGE Model",
        "available_model_layers": [
            "SAM multiplier fallback",
            "calibration prototype",
            "formal model core",
            "AI CGE Chat Studio interface",
            "SML specification layer",
        ],
        "current_solver_options": {
            "sam_multiplier": "ready",
            "gams_runner": "optional",
            "open_source_equilibrium_solver": "placeholder",
            "recursive_dynamic_solver": "placeholder",
        },
        "current_limitations": [
            "Full equilibrium solving is not implemented yet.",
            "Recursive dynamics are placeholders.",
            "GAMS and open-source solver pathways are optional future backends.",
        ],
        "supported_scenario_types": [
            "fiscal_policy",
            "care_economy",
            "infrastructure",
            "trade_policy",
            "productivity",
            "custom_prompt",
        ],
        "supported_account_suffixes": ["fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"],
        "active_backend_status": "python_sam_multiplier_ready",
    }
