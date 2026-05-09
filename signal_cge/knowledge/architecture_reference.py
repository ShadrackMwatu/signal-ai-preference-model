"""Structured references for the canonical Signal CGE architecture."""

from __future__ import annotations

from signal_cge.knowledge.reference_index import build_reference_index


def get_architecture_reference() -> dict[str, object]:
    """Return the canonical architecture map used by Signal AI modules."""

    index = build_reference_index()
    return {
        "engine": "signal_cge",
        "model_layers": [
            "data",
            "calibration",
            "model_core",
            "solvers",
            "scenarios",
            "dynamics",
            "diagnostics",
            "reporting",
            "workbench",
        ],
        "ai_layers": [
            "AI CGE Chat Studio",
            "policy AI",
            "Signal reasoning",
            "learning modules",
            "scenario recommendation engine",
        ],
        "reference_sections": index["sections"],
        "canonical_references": index["canonical_references"],
        "knowledge_base": index.get("knowledge_base"),
    }
