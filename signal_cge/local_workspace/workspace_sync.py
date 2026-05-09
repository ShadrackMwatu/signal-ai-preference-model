"""Synchronization policy helpers for local and repository Signal CGE storage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from signal_cge.local_workspace.workspace_manager import CONFIG_DIR, load_key_value_yaml


SYNC_POLICY_PATH = CONFIG_DIR / "sync_policy.yaml"


def load_sync_policy(path: str | Path = SYNC_POLICY_PATH) -> dict[str, Any]:
    """Load the local workspace synchronization policy."""

    return load_key_value_yaml(path)


def summarize_sync_policy(path: str | Path = SYNC_POLICY_PATH) -> dict[str, object]:
    """Return a compact policy summary for AI and UI modules."""

    policy = load_sync_policy(path)
    return {
        "sync_to_github": policy.get("sync_to_github", []),
        "do_not_sync": policy.get("do_not_sync", []),
        "ignored_patterns": policy.get("ignored_patterns", []),
        "local_artifacts_remain_local": True,
    }


def should_sync_path(path: str | Path, policy_path: str | Path = SYNC_POLICY_PATH) -> bool:
    """Return whether a path is allowed to sync by the configured policy."""

    suffix = Path(path).suffix.lower()
    name = str(path).replace("\\", "/").lower()
    policy = load_sync_policy(policy_path)
    for pattern in policy.get("ignored_patterns", []):
        clean = str(pattern).strip('"').lower()
        if clean.startswith("*.") and suffix == clean[1:]:
            return False
        if clean.endswith("/") and f"/{clean}" in f"/{name}/":
            return False
    return True
