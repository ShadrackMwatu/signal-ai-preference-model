"""Strict privacy filtering for aggregated place intelligence."""

from __future__ import annotations

from typing import Any

FORBIDDEN_FIELDS = {
    "user_id",
    "device_id",
    "imei",
    "phone",
    "route",
    "gps_trace",
    "personal_location",
    "home_location",
    "work_location",
    "individual_coordinates",
    "latitude_history",
    "longitude_history",
    "movement_trail",
    "route_history",
}


def apply_privacy_guard(record: dict[str, Any]) -> dict[str, Any]:
    """Approve only aggregate place intelligence, never personal mobility data."""
    found = sorted({str(key) for key in record if str(key).lower() in FORBIDDEN_FIELDS})
    if found:
        raise ValueError(f"Person-level mobility fields are not allowed: {', '.join(found)}")
    safe = {key: value for key, value in record.items() if str(key).lower() not in FORBIDDEN_FIELDS}
    safe["privacy_status"] = "approved"
    return safe


def assert_no_personal_mobility_data(records: list[dict[str, Any]]) -> None:
    for record in records:
        apply_privacy_guard(record)