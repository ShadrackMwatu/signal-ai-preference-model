"""Privacy safeguards for Signal trend intelligence."""

from __future__ import annotations

from typing import Any


ALLOWED_SIGNAL_LEVELS = (
    "aggregate trends",
    "topic-level signals",
    "location-level public indicators",
    "time-level signals",
)
BLOCKED_PERSONAL_FIELDS = (
    "username",
    "user_id",
    "private_message",
    "profile_url",
    "personal_timeline",
    "display_name",
)
PRIVACY_NOTICE = (
    "Signal only uses aggregate public trends, topic-level signals, location-level indicators, "
    "and time-level observations. It does not store usernames, user ids, private messages, "
    "individual profiles, or personal timelines."
)


def sanitize_trend_record(record: dict[str, Any]) -> dict[str, Any]:
    """Remove any unexpected personal fields from a trend record."""

    return {key: value for key, value in record.items() if key not in BLOCKED_PERSONAL_FIELDS}


def is_privacy_safe_record(record: dict[str, Any]) -> bool:
    return not any(field in record for field in BLOCKED_PERSONAL_FIELDS)


def assert_privacy_safe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [sanitize_trend_record(record) for record in records]
