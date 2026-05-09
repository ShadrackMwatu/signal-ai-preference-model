"""Canonical Signal CGE knowledge access helpers."""

from signal_cge.knowledge.architecture_reference import get_architecture_reference
from signal_cge.knowledge.document_loader import (
    CANONICAL_MODEL_ROOT,
    REFERENCE_ROOT,
    load_model_profile,
    load_reference_text,
    list_reference_documents,
)
from signal_cge.knowledge.reference_index import build_reference_index

__all__ = [
    "CANONICAL_MODEL_ROOT",
    "REFERENCE_ROOT",
    "build_reference_index",
    "get_architecture_reference",
    "list_reference_documents",
    "load_model_profile",
    "load_reference_text",
]
