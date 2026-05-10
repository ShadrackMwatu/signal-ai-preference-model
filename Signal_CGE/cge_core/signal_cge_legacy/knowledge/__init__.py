"""Canonical Signal CGE knowledge access helpers."""

from .architecture_reference import get_architecture_reference
from .document_loader import (
    CANONICAL_MODEL_ROOT,
    REFERENCE_ROOT,
    load_model_profile,
    load_reference_text,
    list_reference_documents,
)
from .reference_index import build_reference_index
from .scenario_context import get_scenario_context
from .semantic_mapping import infer_account_type, map_prompt_semantics
from .knowledge_graph import build_knowledge_graph, get_topic_references

__all__ = [
    "CANONICAL_MODEL_ROOT",
    "REFERENCE_ROOT",
    "build_reference_index",
    "get_architecture_reference",
    "list_reference_documents",
    "load_model_profile",
    "load_reference_text",
    "get_scenario_context",
]
