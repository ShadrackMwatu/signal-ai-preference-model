"""Privacy safeguards for aggregate market-intelligence data."""

from __future__ import annotations

import re

import pandas as pd


MIN_GROUP_SIZE = 30

PII_COLUMNS = {
    "name",
    "email",
    "phone",
    "phone_number",
    "user_id",
    "username",
    "handle",
    "profile_url",
    "ip_address",
    "device_id",
    "national_id",
    "passport",
    "gps",
    "gps_coordinates",
    "latitude",
    "longitude",
    "lat",
    "lon",
    "psychological_profile",
    "psychographic_segment",
    "personality_score",
    "personality_type",
    "microtargeting_score",
}

PII_PATTERNS = (
    re.compile(r"[\w\.-]+@[\w\.-]+\.\w+"),
    re.compile(r"(?:\+?254|0)\d{9}\b"),
)

AGGREGATION_KEYS = ("country", "county", "category", "consumer_segment", "time_period")


def filter_private_data(frame: pd.DataFrame, min_group_size: int = MIN_GROUP_SIZE) -> pd.DataFrame:
    """Validate privacy and suppress rows below a k-anonymity threshold."""

    validate_no_pii(frame)
    safe = suppress_small_groups(frame, min_group_size=min_group_size)
    return safe.reset_index(drop=True)


def suppress_small_groups(frame: pd.DataFrame, min_group_size: int = MIN_GROUP_SIZE) -> pd.DataFrame:
    """Drop aggregate rows whose observation counts are too small."""

    if "observation_count" not in frame.columns:
        raise ValueError("observation_count is required for k-anonymity suppression")
    return frame[frame["observation_count"] >= min_group_size].copy()


def validate_no_pii(frame: pd.DataFrame) -> None:
    """Reject PII columns, direct identifiers, exact GPS, and PII-like text."""

    lower_columns = {column.lower() for column in frame.columns}
    blocked = lower_columns.intersection(PII_COLUMNS)
    if blocked:
        raise ValueError(f"PII or prohibited targeting columns are not allowed: {', '.join(sorted(blocked))}")

    for key in AGGREGATION_KEYS:
        if key not in frame.columns:
            raise ValueError(f"aggregate key is required: {key}")

    if "text" in frame.columns:
        text = " ".join(frame["text"].astype(str).tolist())
        for pattern in PII_PATTERNS:
            if pattern.search(text):
                raise ValueError("PII-like text pattern detected")


def aggregate_only_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return only aggregate-safe output columns."""

    blocked = {"signal_id", "text"}
    safe_columns = [column for column in frame.columns if column not in blocked and column.lower() not in PII_COLUMNS]
    return frame[safe_columns].copy()
