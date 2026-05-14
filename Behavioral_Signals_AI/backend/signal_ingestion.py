"""Behavioral signal ingestion normalization for aggregate public signals."""

from __future__ import annotations

from typing import Any


def ingest_aggregate_trends(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Accept aggregate public records and return sanitized pipeline inputs."""

    blocked = {"username", "user_id", "profile_url", "email", "phone", "text", "raw_post"}
    sanitized = []
    for record in records:
        sanitized.append({key: value for key, value in dict(record).items() if key not in blocked})
    return sanitized