"""Index canonical Signal CGE reference materials for AI and workflow modules."""

from __future__ import annotations

from typing import Any

from .document_loader import (
    KNOWLEDGE_BASE_PATH,
    list_repo_knowledge_sources,
    list_reference_documents,
    load_model_profile,
)
from ..model_registry import get_canonical_reference_registry


def build_reference_index() -> dict[str, Any]:
    """Build a deterministic index of canonical model, guide, and workflow references."""

    documents = list_reference_documents()
    repo_sources = list_repo_knowledge_sources()
    return {
        "model_profile": load_model_profile(),
        "canonical_references": get_canonical_reference_registry(),
        "documents": documents,
        "repo_knowledge_sources": repo_sources,
        "sections": sorted({document["section"] for document in documents}),
        "knowledge_categories": _categorize_sources(repo_sources),
        "knowledge_base": str(KNOWLEDGE_BASE_PATH.relative_to(KNOWLEDGE_BASE_PATH.parents[1])),
    }


def _categorize_sources(sources: list[dict[str, Any]]) -> dict[str, list[str]]:
    categories = {
        "equations": [],
        "calibration": [],
        "closures": [],
        "scenario_templates": [],
        "diagnostics": [],
        "solver_notes": [],
        "workflow_notes": [],
        "policy_interpretation": [],
        "recursive_dynamics": [],
        "sam_validation": [],
    }
    for source in sources:
        path = str(source.get("path", "")).lower()
        target = str(source.get("path", ""))
        if "equation" in path:
            categories["equations"].append(target)
        if "calibration" in path:
            categories["calibration"].append(target)
        if "closure" in path:
            categories["closures"].append(target)
        if "scenario" in path or "experiment" in path:
            categories["scenario_templates"].append(target)
        if "diagnostic" in path or "validation" in path:
            categories["diagnostics"].append(target)
        if "solver" in path or "gams" in path:
            categories["solver_notes"].append(target)
        if "workflow" in path or "guide" in path:
            categories["workflow_notes"].append(target)
        if "policy" in path or "interpretation" in path:
            categories["policy_interpretation"].append(target)
        if "dynamic" in path or "recursive" in path:
            categories["recursive_dynamics"].append(target)
        if "sam" in path or "balance" in path:
            categories["sam_validation"].append(target)
    return categories
