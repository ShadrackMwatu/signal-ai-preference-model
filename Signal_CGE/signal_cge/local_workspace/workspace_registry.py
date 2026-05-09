"""Registry view connecting Signal CGE to the local model workspace."""

from __future__ import annotations

from .workspace_manager import get_workspace_paths, locate_runtime_outputs
from .workspace_sync import summarize_sync_policy
from .workspace_validator import validate_workspace


def get_workspace_registry() -> dict[str, object]:
    """Return local workspace references without loading large artifacts."""

    paths = get_workspace_paths()
    return {
        "storage_authority": {
            "local_model_workspace": "authoritative for runtime model artifacts",
            "github_repository": "authoritative for code, architecture, docs, tests, and lightweight configs",
            "hugging_face": "deployment target for lightweight repository files",
        },
        "local_workspace": {key: str(value) for key, value in paths.items()},
        "runtime_outputs": locate_runtime_outputs(),
        "validation": validate_workspace(),
        "sync_policy": summarize_sync_policy(),
        "artifact_loading_policy": "metadata_only_by_default",
    }
