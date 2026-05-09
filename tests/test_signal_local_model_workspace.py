"""Tests for the local canonical Signal model workspace integration."""

from __future__ import annotations

from pathlib import Path

from signal_cge.local_workspace.workspace_manager import (
    REQUIRED_WORKSPACE_FOLDERS,
    ensure_workspace_structure,
    get_workspace_paths,
)
from signal_cge.local_workspace.workspace_registry import get_workspace_registry
from signal_cge.local_workspace.workspace_sync import load_sync_policy, should_sync_path
from signal_cge.local_workspace.workspace_validator import (
    path_is_runtime_artifact,
    validate_workspace,
)
from signal_cge.model_registry import get_model_registry


def test_local_model_paths_load_and_expand() -> None:
    """Local model config should expand canonical path placeholders."""

    paths = get_workspace_paths()

    assert paths["canonical_model_root"].as_posix().endswith("models/Model")
    assert paths["sam_storage"] == paths["canonical_model_root"] / "sam"
    assert paths["runtime_storage"] == paths["canonical_model_root"] / "runtime"


def test_workspace_structure_exists_or_is_created() -> None:
    """The local persistent workspace should contain all required folders."""

    result = ensure_workspace_structure()
    root = Path(result["workspace_root"])

    assert root.exists()
    for folder in REQUIRED_WORKSPACE_FOLDERS:
        assert (root / folder).exists()


def test_workspace_validator_reports_valid_workspace() -> None:
    """Workspace validation should report missing folders and large-artifact policy."""

    result = validate_workspace()

    assert result["is_valid"] is True
    assert result["missing_folders"] == []
    assert result["large_artifacts_policy"] == "local_only"


def test_sync_policy_loading_and_decision_rules() -> None:
    """Synchronization policy should block runtime artifacts."""

    policy = load_sync_policy()

    assert ".gdx" in policy["do_not_sync"]
    assert "*.gdx" in policy["ignored_patterns"]
    assert should_sync_path("signal_cge/model_registry.py") is True
    assert should_sync_path("models/Model/runtime/run.gdx") is False
    assert should_sync_path("models/Model/outputs/solver.log") is False


def test_runtime_artifact_detection() -> None:
    """Runtime paths and solver extensions should be classified as local-only."""

    assert path_is_runtime_artifact("models/Model/checkpoints/base.gdx") is True
    assert path_is_runtime_artifact("models/Model/scenarios/policy.yaml") is False


def test_model_registry_references_local_and_repo_storage() -> None:
    """The central registry should expose both repo and local workspace storage."""

    registry = get_model_registry()

    assert "canonical_repo_models" in registry
    assert "local_workspace" in registry
    assert registry["local_workspace"]["artifact_loading_policy"] == "metadata_only_by_default"
    assert registry["local_workspace"]["storage_authority"]["local_model_workspace"].startswith(
        "authoritative"
    )


def test_safe_ignore_behavior_is_documented_in_gitignore() -> None:
    """Large model artifacts should be protected by ignore rules."""

    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    for pattern in ["models/Model/", "*.gdx", "*.g00", "*.lst", "runtime/", "checkpoints/"]:
        assert pattern in gitignore


def test_app_import_still_works() -> None:
    """The Hugging Face app entrypoint should remain importable."""

    import app  # noqa: PLC0415

    assert hasattr(app, "demo")
