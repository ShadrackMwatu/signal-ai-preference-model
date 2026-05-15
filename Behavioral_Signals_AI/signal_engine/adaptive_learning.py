"""Adaptive learning rules for processed topical signals."""

from __future__ import annotations

from collections import Counter
from typing import Any


def topic_key(topic: str) -> str:
    return " ".join(str(topic).lower().strip().split())


def summarize_prior_topics(memory: list[dict[str, Any]]) -> Counter:
    return Counter(topic_key(item.get("signal_topic") or item.get("topic") or "") for item in memory if item)


def persistence_for_topic(topic: str, memory: list[dict[str, Any]]) -> float:
    counts = summarize_prior_topics(memory)
    count = counts.get(topic_key(topic), 0)
    return min(95.0, 45.0 + count * 12.0)


def source_confirmation_for_topic(topic: str, records: list[dict[str, Any]]) -> int:
    key = topic_key(topic)
    sources = {
        str(record.get("source_type") or record.get("source") or "aggregate_public")
        for record in records
        if topic_key(record.get("topic") or record.get("signal_name") or record.get("trend_name") or "") == key
    }
    return max(1, len(sources))