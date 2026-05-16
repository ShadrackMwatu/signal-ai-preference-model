"""Privacy filter for massive aggregate intelligence ingestion.

Principle: collect massive aggregate intelligence, not personal data.
"""

from __future__ import annotations

import re
from typing import Any

FORBIDDEN_FIELDS = {
    "name", "names", "phone", "phone_number", "email", "device_id", "imei", "user_id",
    "private_message", "individual_searches", "exact_personal_location", "exact_location",
    "personal_routes", "route", "gps_trace", "individual_profiles", "personal_profile",
}

PRIVATE_PATTERNS = [
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
    re.compile(r"\b(device_id|user_id|private_message|gps_trace|personal_profile)\b", re.IGNORECASE),
]


def apply_ingestion_privacy_filter(record: dict[str, Any]) -> dict[str, Any] | None:
    """Redact private text and reject records containing person-level fields."""
    if not isinstance(record, dict):
        return None
    lowered_keys = {str(key).lower() for key in record}
    if lowered_keys.intersection(FORBIDDEN_FIELDS):
        return None
    cleaned = {str(key): _redact(value) for key, value in record.items() if str(key).lower() not in FORBIDDEN_FIELDS}
    cleaned["privacy_level"] = "aggregate"
    if any(_contains_private_text(value) for value in cleaned.values()):
        return None
    return cleaned


def assert_no_private_fields(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_FIELDS or not assert_no_private_fields(item):
                return False
    elif isinstance(value, list):
        return all(assert_no_private_fields(item) for item in value)
    elif isinstance(value, str):
        return not _contains_private_text(value)
    return True


def _redact(value: Any) -> Any:
    if isinstance(value, str):
        text = value
        for pattern in PRIVATE_PATTERNS:
            text = pattern.sub("[redacted]", text)
        return text
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, dict):
        return {key: _redact(item) for key, item in value.items() if str(key).lower() not in FORBIDDEN_FIELDS}
    return value


def _contains_private_text(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in PRIVATE_PATTERNS)
