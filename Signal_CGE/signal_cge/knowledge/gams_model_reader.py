"""Read local Signal CGE GAMS model metadata for repo-safe intelligence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..local_model.local_model_detector import detect_local_signal_cge_model
from ..local_model.model_gms_parser import parse_model_gms_metadata


OUTPUT_PATH = Path("Signal_CGE/outputs/model_intelligence/model_gms_metadata.json")


def read_gams_model_intelligence(model_file: str | Path | None = None, write: bool = True) -> dict[str, Any]:
    """Read model.gms and return lightweight structural metadata."""

    detection = detect_local_signal_cge_model()
    path = Path(model_file) if model_file else Path(detection["model_file"])
    metadata = parse_model_gms_metadata(path)
    metadata["local_model_detected"] = detection["local_model_detected"]
    metadata["active_sam_file"] = detection["active_sam_file"]
    if write:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata
