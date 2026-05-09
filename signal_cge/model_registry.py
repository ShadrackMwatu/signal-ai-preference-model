"""Central registry for Signal CGE model layers, references, and capabilities."""

from __future__ import annotations

from pathlib import Path

from signal_cge.local_workspace.workspace_registry import get_workspace_registry


REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = REPO_ROOT / "Documentation" / "signal_cge_reference"
CANONICAL_MODEL_ROOT = REPO_ROOT / "models" / "canonical"


def get_canonical_reference_registry() -> dict[str, object]:
    """Return canonical documentation and model-profile paths for Signal CGE."""

    return {
        "reference_root": str(REFERENCE_ROOT),
        "user_guides": {
            "root_adapted_docx": str(REPO_ROOT / "Documentation" / "Signal_CGE_User_Guide_Adapted.docx"),
            "root_adapted_pdf": str(REPO_ROOT / "Documentation" / "Signal_CGE_User_Guide_Adapted.pdf"),
            "adapted_docx": str(
                REFERENCE_ROOT / "user_guides" / "Signal_CGE_User_Guide_Adapted.docx"
            ),
            "adapted_pdf": str(
                REFERENCE_ROOT / "user_guides" / "Signal_CGE_User_Guide_Adapted.pdf"
            ),
        },
        "knowledge_base": str(REPO_ROOT / "Documentation" / "SIGNAL_CGE_KNOWLEDGE_BASE.md"),
        "architecture_docs": str(REFERENCE_ROOT / "architecture"),
        "calibration_docs": str(REFERENCE_ROOT / "calibration"),
        "equation_docs": str(REFERENCE_ROOT / "equations"),
        "experiment_templates": str(CANONICAL_MODEL_ROOT / "experiment_templates"),
        "closure_templates": str(REFERENCE_ROOT / "closures"),
        "model_profile": str(CANONICAL_MODEL_ROOT / "signal_cge_master" / "model_profile.yaml"),
    }


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
        "canonical_model_structure": "signal_cge",
        "canonical_references": get_canonical_reference_registry(),
        "canonical_repo_models": {
            "root": str(CANONICAL_MODEL_ROOT),
            "signal_cge_master": str(CANONICAL_MODEL_ROOT / "signal_cge_master"),
            "templates": str(CANONICAL_MODEL_ROOT / "templates"),
            "calibration_profiles": str(CANONICAL_MODEL_ROOT / "calibration_profiles"),
            "experiment_templates": str(CANONICAL_MODEL_ROOT / "experiment_templates"),
        },
        "local_workspace": get_workspace_registry(),
    }
