"""Privacy-preserving filters for aggregate signal records."""

from __future__ import annotations

from typing import Any

PRIVACY_NOTE = "Signal uses aggregate, anonymized, public, or user-authorized data sources. It does not identify, track, or profile individuals."

BLOCKED_FIELDS = {
    "user_id",
    "email",
    "phone",
    "private_message",
    "exact_location",
    "personal_profile",
    "name",
    "ip_address",
    "device_id",
}


def sanitize_aggregate_record(record: dict[str, Any]) -> dict[str, Any]:
    safe = {str(key): value for key, value in dict(record or {}).items() if str(key).lower() not in BLOCKED_FIELDS}
    safe["privacy_level"] = "aggregate_public"
    return safe


def validate_privacy_safe_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    present = sorted(field for field in BLOCKED_FIELDS if field in {str(key).lower() for key in dict(record or {})})
    return not present, present