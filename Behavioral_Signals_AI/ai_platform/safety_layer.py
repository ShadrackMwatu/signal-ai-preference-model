"""Privacy and safety helpers for Open Signals platform orchestration."""

from __future__ import annotations

import re
from typing import Any

PRIVATE_DATA_RESPONSE = (
    "Open Signals only works with aggregate, anonymized, public, or user-authorized intelligence. "
    "I cannot identify individuals or expose private behavior."
)

FORBIDDEN_FIELD_NAMES = {
    "user_id",
    "device_id",
    "imei",
    "email",
    "phone",
    "private_message",
    "personal_profile",
    "exact_location",
    "gps",
    "gps_trace",
    "route",
    "home_location",
    "work_location",
    "individual_profile",
    "individual_searches",
    "raw_likes",
    "raw_comments",
    "raw_shares",
}

FORBIDDEN_PROMPT_PATTERNS = [
    re.compile(r"\b(user_id|device_id|imei|phone|email|private_message|personal_profile|exact location|gps|route|home address|work address|raw likes|raw comments|raw shares|raw searches|individual profile)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
]


def is_privacy_sensitive_prompt(message: str) -> bool:
    return any(pattern.search(str(message or "")) for pattern in FORBIDDEN_PROMPT_PATTERNS)


def sanitize_context(value: Any) -> Any:
    """Remove private field names and private-looking text from nested context."""
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_FIELD_NAMES:
                continue
            cleaned[key_text] = sanitize_context(item)
        return cleaned
    if isinstance(value, list):
        return [sanitize_context(item) for item in value[:50]]
    if isinstance(value, tuple):
        return [sanitize_context(item) for item in value[:50]]
    if isinstance(value, str):
        text = value
        for pattern in FORBIDDEN_PROMPT_PATTERNS:
            text = pattern.sub("[private field removed]", text)
        return text[:1200]
    return value


def context_contains_private_fields(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in FORBIDDEN_FIELD_NAMES or context_contains_private_fields(item) for key, item in value.items())
    if isinstance(value, list):
        return any(context_contains_private_fields(item) for item in value)
    if isinstance(value, str):
        return is_privacy_sensitive_prompt(value)
    return False
