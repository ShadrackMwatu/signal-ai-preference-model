"""Validate local Signal CGE model workspace availability and safety."""

from __future__ import annotations

from pathlib import Path

from signal_cge.local_workspace.workspace_manager import (
    REQUIRED_WORKSPACE_FOLDERS,
    get_workspace_paths,
)


def validate_workspace(create_missing: bool = False) -> dict[str, object]:
    """Validate that the local persistent model workspace is available."""

    paths = get_workspace_paths()
    root = paths["canonical_model_root"]
    missing = [folder for folder in REQUIRED_WORKSPACE_FOLDERS if not (root / folder).exists()]
    if create_missing:
        for folder in missing:
            (root / folder).mkdir(parents=True, exist_ok=True)
        missing = []

    return {
        "workspace_root": str(root),
        "exists": root.exists(),
        "missing_folders": missing,
        "is_valid": root.exists() and not missing,
        "large_artifacts_policy": "local_only",
    }


def path_is_runtime_artifact(path: str | Path) -> bool:
    """Return whether a path should be treated as local runtime output."""

    path_obj = Path(path)
    runtime_names = {"outputs", "checkpoints", "archives", "runtime"}
    runtime_extensions = {".gdx", ".g00", ".lst", ".log", ".tmp", ".bak"}
    return bool(runtime_names.intersection(path_obj.parts)) or path_obj.suffix.lower() in runtime_extensions
