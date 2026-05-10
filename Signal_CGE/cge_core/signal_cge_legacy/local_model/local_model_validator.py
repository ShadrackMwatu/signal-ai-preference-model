"""Validation for local Signal CGE model structure."""

from __future__ import annotations

from typing import Any

from .local_model_detector import detect_local_signal_cge_model


def validate_local_signal_cge_structure(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate required and optional local Signal CGE model files."""

    detected = detect_local_signal_cge_model(config)
    required = {
        "model.gms": detected["model_file_exists"],
        "20_Data": detected["data_folder_exists"],
        "KEN_SAM_2020.xlsx": detected["active_sam_exists"],
    }
    optional = {key: value["exists"] for key, value in detected["optional_folders"].items()}
    return {
        "valid": all(required.values()),
        "required": required,
        "optional": optional,
        "detected": detected,
        "warnings": detected["warnings"],
    }
