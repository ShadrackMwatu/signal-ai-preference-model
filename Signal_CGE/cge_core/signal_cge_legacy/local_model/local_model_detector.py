"""Detect the active local Signal CGE model files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .local_model_config import candidate_model_roots, load_local_signal_cge_config


def detect_local_signal_cge_model(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Detect model root, model.gms, data folder, SAM, and optional folders."""

    config = config or load_local_signal_cge_config()
    selected_root: Path | None = None
    for candidate in candidate_model_roots(config):
        if (candidate / str(config["main_model_file"])).exists() or (
            candidate / str(config["data_folder"]) / str(config["active_sam_file"])
        ).exists():
            selected_root = candidate
            break
    selected_root = selected_root or candidate_model_roots(config)[0]
    data_folder = selected_root / str(config["data_folder"])
    model_file = selected_root / str(config["main_model_file"])
    active_sam = data_folder / str(config["active_sam_file"])
    optional_folders = {
        "save_folder": _folder_variant(selected_root, str(config["save_folder"])),
        "gdx_folder": _folder_variant(selected_root, str(config["gdx_folder"])),
        "result_folder": _folder_variant(selected_root, str(config["result_folder"])),
    }
    return {
        "local_model_detected": bool(model_file.exists() or active_sam.exists()),
        "model_root": str(selected_root),
        "model_file": str(model_file),
        "model_file_exists": model_file.exists(),
        "data_folder": str(data_folder),
        "data_folder_exists": data_folder.exists(),
        "active_sam_file": str(active_sam),
        "active_sam_exists": active_sam.exists(),
        "optional_folders": {key: {"path": str(path), "exists": path.exists()} for key, path in optional_folders.items()},
        "config": config,
        "warnings": _warnings(model_file, data_folder, active_sam),
    }


def _folder_variant(root: Path, folder: str) -> Path:
    direct = root / folder
    if direct.exists():
        return direct
    lower = root / folder.lower()
    if lower.exists():
        return lower
    return direct


def _warnings(model_file: Path, data_folder: Path, active_sam: Path) -> list[str]:
    warnings: list[str] = []
    if not model_file.exists():
        warnings.append("Active Signal CGE GAMS model file was not found.")
    if not data_folder.exists():
        warnings.append("Active Signal CGE data folder was not found.")
    if not active_sam.exists():
        warnings.append("Active Signal CGE SAM workbook was not found.")
    return warnings
