"""SAM loading and validation helpers for Signal CGE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from ..local_model.local_model_detector import detect_local_signal_cge_model


SHEET_PRIORITY = ["SAM", "Disaggregated_SAM", "Balanced_SAM"]
RUNTIME_DIAGNOSTICS = Path("Signal_CGE/outputs/runtime/sam_diagnostics.json")


def load_sam(path: str | Path) -> pd.DataFrame:
    """Load a SAM matrix from CSV or Excel using the first column as accounts."""

    source = Path(path)
    if source.suffix.lower() in {".xlsx", ".xls"}:
        sheet = detect_sam_sheet(source)
        frame = pd.read_excel(source, sheet_name=sheet, index_col=0)
    else:
        frame = pd.read_csv(source, index_col=0)
    frame.index = [str(account).strip() for account in frame.index]
    frame.columns = [str(account).strip() for account in frame.columns]
    return frame.apply(pd.to_numeric, errors="coerce").fillna(0.0).astype(float)


def default_sam_path() -> Path:
    """Return the detected active Signal CGE SAM path."""

    return Path(detect_local_signal_cge_model()["active_sam_file"])


def load_default_signal_sam() -> pd.DataFrame:
    """Load the active local/repo Signal CGE SAM workbook."""

    path = default_sam_path()
    if not path.exists():
        raise FileNotFoundError(f"Active Signal CGE SAM was not found: {path}")
    return load_sam(path)


def detect_sam_sheet(path: str | Path) -> str:
    """Detect the SAM worksheet using Signal's priority order."""

    workbook = pd.ExcelFile(path)
    for sheet in SHEET_PRIORITY:
        if sheet in workbook.sheet_names:
            return sheet
    return workbook.sheet_names[0]


def validate_signal_sam(path_or_frame: str | Path | pd.DataFrame | None = None) -> dict[str, Any]:
    """Load and validate the active SAM without crashing hosted runtimes."""

    try:
        source_path = default_sam_path() if path_or_frame is None else path_or_frame
        frame = load_sam(source_path) if not isinstance(source_path, pd.DataFrame) else source_path.copy()
        labels_match = list(map(str, frame.index)) == list(map(str, frame.columns))
        row_totals = frame.sum(axis=1)
        column_totals = frame.sum(axis=0)
        imbalance = row_totals - column_totals
        diagnostics = {
            "sam_loaded": True,
            "sam_file": Path(str(source_path)).name if not isinstance(source_path, pd.DataFrame) else "dataframe",
            "sam_path": str(source_path) if not isinstance(source_path, pd.DataFrame) else "",
            "sheet": detect_sam_sheet(source_path) if not isinstance(source_path, pd.DataFrame) and Path(str(source_path)).suffix.lower() in {".xlsx", ".xls"} else "",
            "dimensions": [int(frame.shape[0]), int(frame.shape[1])],
            "number_of_accounts": int(frame.shape[0]),
            "row_column_labels_match": labels_match,
            "balanced": bool(labels_match and float(imbalance.abs().max()) <= 1e-6),
            "max_imbalance": float(imbalance.abs().max()),
            "zero_row_count": int((row_totals.abs() <= 1e-12).sum()),
            "zero_column_count": int((column_totals.abs() <= 1e-12).sum()),
            "negative_entry_count": int((frame < 0).sum().sum()),
            "warnings": [] if labels_match else ["SAM row and column labels do not match."],
        }
    except Exception as exc:
        diagnostics = {
            "sam_loaded": False,
            "sam_file": "KEN_SAM_2020.xlsx",
            "sam_path": str(default_sam_path()),
            "sheet": "",
            "dimensions": [0, 0],
            "number_of_accounts": 0,
            "row_column_labels_match": False,
            "balanced": False,
            "max_imbalance": None,
            "zero_row_count": 0,
            "zero_column_count": 0,
            "negative_entry_count": 0,
            "warnings": [str(exc)],
        }
    write_sam_diagnostics(diagnostics)
    return diagnostics


def write_sam_diagnostics(diagnostics: dict[str, Any], path: str | Path = RUNTIME_DIAGNOSTICS) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    return str(target)
