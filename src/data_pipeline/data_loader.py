"""CSV loading and schema validation for behavioral signals."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .privacy_filter import filter_private_data, validate_no_pii


REQUIRED_SIGNAL_COLUMNS = {
    "signal_id",
    "country",
    "county",
    "category",
    "consumer_segment",
    "time_period",
    "observation_count",
    "text",
    "clicks",
    "likes",
    "comments",
    "shares",
    "saves",
    "views",
    "searches",
    "hashtags",
    "mentions",
    "complaints",
    "purchase_intent_phrases",
    "repeated_engagement",
    "ignored_content",
    "delayed_responses",
}


def load_behavioral_signals(path: str | Path, *, apply_privacy_filter: bool = True) -> pd.DataFrame:
    """Load anonymized behavioral signals from CSV."""

    frame = pd.read_csv(path)
    validate_required_columns(frame)
    validate_no_pii(frame)
    if apply_privacy_filter:
        return filter_private_data(frame)
    return frame


def validate_required_columns(frame: pd.DataFrame) -> None:
    """Validate that all required raw-signal fields exist."""

    missing = REQUIRED_SIGNAL_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
