"""Canonical SAM discovery and loading utilities for Signal CGE.

Production priority:
1. user-uploaded SAM path,
2. repository canonical SAM path,
3. bundled demo SAM for tests and safe fallback only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

CANONICAL_SAM_CANDIDATES = (
    Path("Signal_CGE/models/Model/20_Data/KEN_SAM_2020.xlsx"),
    Path("Signal_CGE/models/Model/20_Data/KEN_SAM_2020.xls"),
    Path("Signal_CGE/models/Model/20_Data/KEN_SAM_2020.csv"),
    Path("Signal_CGE/models/canonical/KEN_SAM_2020.xlsx"),
    Path("Signal_CGE/data/sams/raw/KEN_SAM_2020.xlsx"),
    Path("data/sams/raw/KEN_SAM_2020.xlsx"),
)

DEMO_SAM = pd.DataFrame(
    [
        [0, 25, 12, 8, 10, 5],
        [20, 0, 15, 5, 8, 4],
        [14, 18, 0, 6, 10, 7],
        [8, 6, 4, 0, 5, 3],
        [9, 7, 8, 4, 0, 6],
        [6, 5, 7, 3, 6, 0],
    ],
    index=["paid_care_services", "manufacturing", "transport", "health", "households", "government"],
    columns=["paid_care_services", "manufacturing", "transport", "health", "households", "government"],
    dtype=float,
)


@dataclass(frozen=True)
class SAMSource:
    """Resolved SAM source metadata."""

    path: Path | None
    source_type: str
    message: str


def discover_sam_path(uploaded_path: str | Path | None = None, repo_root: str | Path | None = None) -> SAMSource:
    """Resolve uploaded/canonical SAM path without throwing when none exists."""

    root = Path(repo_root or ".").resolve()
    if uploaded_path:
        candidate = Path(uploaded_path)
        if candidate.exists():
            return SAMSource(candidate, "uploaded", f"Using uploaded SAM: {candidate}")
        return SAMSource(None, "missing_uploaded", f"Uploaded SAM path was provided but not found: {candidate}")

    for relative in CANONICAL_SAM_CANDIDATES:
        candidate = relative if relative.is_absolute() else root / relative
        if candidate.exists():
            return SAMSource(candidate, "repo_canonical", f"Using repository canonical SAM: {candidate}")

    return SAMSource(None, "demo", "No uploaded or repository SAM found; demo SAM is available for tests/fallback only.")


def load_sam(path: str | Path) -> pd.DataFrame:
    """Load a SAM matrix from CSV or Excel using the first column as accounts."""

    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"SAM file not found: {source}")
    suffix = source.suffix.lower()
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        frame = pd.read_excel(source, index_col=0)
    elif suffix in {".csv", ".txt"}:
        frame = pd.read_csv(source, index_col=0)
    else:
        raise ValueError(f"Unsupported SAM file type: {suffix}")
    frame.index = [str(account).strip() for account in frame.index]
    frame.columns = [str(account).strip() for account in frame.columns]
    return frame.apply(pd.to_numeric, errors="raise").astype(float)


def load_best_available_sam(uploaded_path: str | Path | None = None, allow_demo: bool = True) -> tuple[pd.DataFrame, SAMSource]:
    """Load uploaded/canonical SAM first; use demo SAM only when allowed."""

    source = discover_sam_path(uploaded_path)
    if source.path is not None:
        return load_sam(source.path), source
    if allow_demo:
        return DEMO_SAM.copy(), source
    raise FileNotFoundError(source.message)


def get_sam_status(uploaded_path: str | Path | None = None) -> dict[str, Any]:
    """Return SAM availability, balance, and structural readiness metadata."""

    source = discover_sam_path(uploaded_path)
    status: dict[str, Any] = {
        "source_type": source.source_type,
        "path": str(source.path) if source.path else "",
        "found": source.path is not None,
        "message": source.message,
        "square": False,
        "balanced": False,
        "max_row_column_gap": None,
        "zero_column_accounts": [],
        "account_count": 0,
    }
    try:
        sam = load_sam(source.path) if source.path else DEMO_SAM.copy()
        row_totals = sam.sum(axis=1)
        col_totals = sam.sum(axis=0)
        common = row_totals.index.intersection(col_totals.index)
        gaps = (row_totals.loc[common] - col_totals.loc[common]).abs() if len(common) else pd.Series(dtype=float)
        status.update(
            {
                "square": sam.shape[0] == sam.shape[1] and list(sam.index) == list(sam.columns),
                "balanced": bool((not gaps.empty) and float(gaps.max()) <= 1e-6),
                "max_row_column_gap": float(gaps.max()) if not gaps.empty else None,
                "zero_column_accounts": col_totals[col_totals == 0].index.astype(str).tolist(),
                "account_count": int(sam.shape[0]),
            }
        )
    except Exception as exc:  # pragma: no cover - defensive readiness path
        status["message"] = f"{source.message} Validation failed: {exc}"
    return status
