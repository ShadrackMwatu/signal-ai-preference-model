"""Index canonical Signal CGE reference materials for AI and workflow modules."""

from __future__ import annotations

from typing import Any

from signal_cge.knowledge.document_loader import (
    KNOWLEDGE_BASE_PATH,
    list_reference_documents,
    load_model_profile,
)
from signal_cge.model_registry import get_canonical_reference_registry


def build_reference_index() -> dict[str, Any]:
    """Build a deterministic index of canonical model, guide, and workflow references."""

    documents = list_reference_documents()
    return {
        "model_profile": load_model_profile(),
        "canonical_references": get_canonical_reference_registry(),
        "documents": documents,
        "sections": sorted({document["section"] for document in documents}),
        "knowledge_base": str(KNOWLEDGE_BASE_PATH.relative_to(KNOWLEDGE_BASE_PATH.parents[1])),
    }
