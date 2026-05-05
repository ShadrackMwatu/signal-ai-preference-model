"""Data preparation helpers for Signal machine-learning workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_NUMERIC_FILL_VALUE = 0.0
PII_COLUMNS = {
    "name",
    "username",
    "email",
    "phone",
    "phone_number",
    "user_id",
    "gps",
    "latitude",
    "longitude",
}


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV or Excel dataset for ML training."""

    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")
    if source.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(source)
    return pd.read_csv(source)


def validate_no_pii_columns(frame: pd.DataFrame) -> None:
    """Block direct identifiers before data is used for model training."""

    lower_columns = {str(column).lower() for column in frame.columns}
    blocked = sorted(lower_columns.intersection(PII_COLUMNS))
    if blocked:
        raise ValueError(f"PII columns are not allowed in Signal ML datasets: {', '.join(blocked)}")


def clean_behavioral_frame(
    frame: pd.DataFrame,
    numeric_columns: Iterable[str] | None = None,
    fill_value: float = DEFAULT_NUMERIC_FILL_VALUE,
) -> pd.DataFrame:
    """Return a copy with PII blocked, numeric values coerced, and missing values filled."""

    validate_no_pii_columns(frame)
    cleaned = frame.copy()
    columns = list(numeric_columns or cleaned.select_dtypes(include="number").columns)
    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").fillna(fill_value)
    return cleaned


def split_features_target(
    frame: pd.DataFrame,
    target_column: str,
    feature_columns: Iterable[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """Split a frame into features and target with clear validation errors."""

    if target_column not in frame.columns:
        raise ValueError(f"Target column not found: {target_column}")
    columns = list(feature_columns or [column for column in frame.columns if column != target_column])
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Feature column(s) not found: {', '.join(missing)}")
    return frame[columns].copy(), frame[target_column].copy()
