"""Manage the local persistent Signal CGE model workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PACKAGE_ROOT / "config"
LOCAL_PATHS_CONFIG = CONFIG_DIR / "local_model_paths.yaml"
REQUIRED_WORKSPACE_FOLDERS = [
    "canonical",
    "calibration",
    "closures",
    "experiments",
    "scenarios",
    "sam",
    "outputs",
    "checkpoints",
    "archives",
    "runtime",
]


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def load_key_value_yaml(path: str | Path) -> dict[str, Any]:
    """Load the simple YAML shape used by Signal workspace configs."""

    config_path = Path(path)
    parsed: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            parsed.setdefault(current_key, []).append(_strip_quotes(stripped[2:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            parsed[current_key] = [] if value == "" else _strip_quotes(value)
    return parsed


def _expand_placeholders(config: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(config)
    for _ in range(3):
        for key, value in list(expanded.items()):
            if not isinstance(value, str):
                continue
            for source_key, source_value in expanded.items():
                if isinstance(source_value, str):
                    value = value.replace("${" + source_key + "}", source_value)
            expanded[key] = value
    return expanded


def get_workspace_paths(config_path: str | Path = LOCAL_PATHS_CONFIG) -> dict[str, Path]:
    """Return resolved local workspace paths from `local_model_paths.yaml`."""

    config = _expand_placeholders(load_key_value_yaml(config_path))
    return {
        key: Path(value)
        for key, value in config.items()
        if isinstance(value, str) and (key.endswith("_storage") or key == "canonical_model_root")
    }


def ensure_workspace_structure(config_path: str | Path = LOCAL_PATHS_CONFIG) -> dict[str, object]:
    """Create the expected local workspace folders if they are missing."""

    paths = get_workspace_paths(config_path)
    root = paths["canonical_model_root"]
    created: list[str] = []
    for folder in REQUIRED_WORKSPACE_FOLDERS:
        path = root / folder
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(path))
    return {
        "workspace_root": str(root),
        "created": created,
        "required_folders": REQUIRED_WORKSPACE_FOLDERS,
    }


def locate_runtime_outputs(config_path: str | Path = LOCAL_PATHS_CONFIG) -> dict[str, str]:
    """Return output, checkpoint, archive, and runtime locations."""

    paths = get_workspace_paths(config_path)
    return {
        "outputs": str(paths["output_storage"]),
        "checkpoints": str(paths["checkpoint_storage"]),
        "archives": str(paths["archive_storage"]),
        "runtime": str(paths["runtime_storage"]),
    }
