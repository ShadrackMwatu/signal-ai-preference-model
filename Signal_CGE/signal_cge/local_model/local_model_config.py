"""Configuration loader for the local Signal CGE model workspace."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO_ROOT / "signal_cge" / "config" / "local_signal_cge_model.yaml"
PACKAGE_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "local_signal_cge_model.yaml"


def load_local_signal_cge_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load local model config, honoring SIGNAL_CGE_LOCAL_MODEL_ROOT."""

    path = Path(config_path) if config_path else PACKAGE_CONFIG_PATH
    config = _parse_key_value_yaml(path.read_text(encoding="utf-8")) if path.exists() else {}
    config.setdefault("model_root", "models/Model")
    config.setdefault("main_model_file", "model.gms")
    config.setdefault("data_folder", "20_Data")
    config.setdefault("active_sam_file", "KEN_SAM_2020.xlsx")
    config.setdefault("region_code", "KEN")
    config.setdefault("save_folder", "00_Save")
    config.setdefault("gdx_folder", "10_gdx")
    config.setdefault("result_folder", "70_Result")
    config.setdefault("base_save_name", "KEN_Base")
    config.setdefault("base_debug_gdx", "KENBaseDebug")
    config.setdefault("base_reference_file", "KENBaseRef")
    override = os.environ.get("SIGNAL_CGE_LOCAL_MODEL_ROOT", "").strip()
    if override:
        config["model_root"] = override
        config["model_root_source"] = "SIGNAL_CGE_LOCAL_MODEL_ROOT"
    else:
        config["model_root_source"] = "config"
    return config


def candidate_model_roots(config: dict[str, Any] | None = None) -> list[Path]:
    """Return repo-safe candidate roots for the local model."""

    config = config or load_local_signal_cge_config()
    raw_root = Path(str(config["model_root"]))
    candidates = []
    if raw_root.is_absolute():
        candidates.append(raw_root)
    else:
        candidates.extend(
            [
                REPO_ROOT / raw_root,
                REPO_ROOT / "Signal_CGE" / raw_root,
                REPO_ROOT / "Signal_CGE" / "models" / "Model" / "Model",
                REPO_ROOT / "models" / "Model",
            ]
        )
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if str(resolved) not in seen:
            unique.append(resolved)
            seen.add(str(resolved))
    return unique


def _parse_key_value_yaml(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values
