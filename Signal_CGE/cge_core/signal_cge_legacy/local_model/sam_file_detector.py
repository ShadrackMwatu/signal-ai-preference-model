"""SAM file detection for the local Signal CGE model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .local_model_detector import detect_local_signal_cge_model


def detect_active_sam_file(model_detection: dict[str, Any] | None = None) -> dict[str, Any]:
    """Detect the active SAM workbook and nearby candidate workbooks."""

    detected = model_detection or detect_local_signal_cge_model()
    data_folder = Path(str(detected["data_folder"]))
    active = Path(str(detected["active_sam_file"]))
    candidates = sorted(data_folder.glob("*.xlsx")) if data_folder.exists() else []
    return {
        "active_sam_file": str(active),
        "active_sam_name": active.name,
        "active_sam_exists": active.exists(),
        "data_folder": str(data_folder),
        "candidate_workbooks": [str(path) for path in candidates],
        "warnings": [] if active.exists() else ["Active SAM workbook was not found."],
    }
