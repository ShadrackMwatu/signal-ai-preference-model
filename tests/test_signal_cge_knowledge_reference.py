"""Tests for the canonical Signal CGE knowledge and reference layer."""

from __future__ import annotations

from pathlib import Path

from signal_cge.knowledge.architecture_reference import get_architecture_reference
from signal_cge.knowledge.document_loader import (
    MODEL_PROFILE_PATH,
    REFERENCE_ROOT,
    load_model_profile,
    load_reference_text,
    list_reference_documents,
)
from signal_cge.knowledge.reference_index import build_reference_index
from signal_cge.model_registry import get_model_registry


def test_canonical_reference_paths_exist() -> None:
    """The adapted user guides and model profile should be available."""

    user_guides = REFERENCE_ROOT / "user_guides"

    assert (user_guides / "Signal_CGE_User_Guide_Adapted.docx").exists()
    assert (user_guides / "Signal_CGE_User_Guide_Adapted.pdf").exists()
    assert MODEL_PROFILE_PATH.exists()


def test_model_profile_parses_without_yaml_dependency() -> None:
    """The canonical YAML profile should parse through the lightweight loader."""

    profile = load_model_profile()

    assert profile["model_identity"] == "Signal CGE"
    assert profile["model_type"] == "recursive_dynamic_single_country_cge"
    assert "Python SAM multiplier fallback" in profile["solver_pathways"]
    assert "care economy" in profile["supported_scenarios"]


def test_reference_index_lists_key_sections() -> None:
    """The document index should expose the canonical reference sections."""

    index = build_reference_index()

    assert "documents" in index
    assert "equations" in index["sections"]
    assert "calibration" in index["sections"]
    assert any(
        document["path"].endswith("CALIBRATION_PIPELINE.md")
        for document in index["documents"]
    )


def test_document_loader_reads_reference_text() -> None:
    """Reference text loading should stay rooted in the canonical docs directory."""

    text = load_reference_text("calibration/CALIBRATION_PIPELINE.md")

    assert "SAM Loading" in text
    assert "Replication Checks" in text


def test_model_registry_exposes_canonical_references() -> None:
    """The model registry should connect Signal to canonical documentation."""

    registry = get_model_registry()
    references = registry["canonical_references"]

    assert registry["canonical_model_structure"] == "signal_cge"
    assert references["model_profile"].endswith("model_profile.yaml")
    assert references["equation_docs"].endswith(str(Path("signal_cge_reference") / "equations"))


def test_architecture_reference_exposes_ai_layers() -> None:
    """Future AI integrations should be able to discover the canonical architecture."""

    architecture = get_architecture_reference()

    assert architecture["engine"] == "signal_cge"
    assert "model_core" in architecture["model_layers"]
    assert "AI CGE Chat Studio" in architecture["ai_layers"]


def test_reference_availability_includes_user_guides() -> None:
    """The reference document list should include the adapted Word and PDF guides."""

    documents = list_reference_documents()
    paths = {document["path"] for document in documents}

    assert any(path.endswith("Signal_CGE_User_Guide_Adapted.docx") for path in paths)
    assert any(path.endswith("Signal_CGE_User_Guide_Adapted.pdf") for path in paths)
