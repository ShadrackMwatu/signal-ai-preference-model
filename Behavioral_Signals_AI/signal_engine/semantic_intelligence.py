"""Semantic intelligence for related Kenya demand signals."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from typing import Any

THEME_SYNONYMS = {
    "Affordable smartphone demand": ["cheap smartphone", "budget android", "affordable smartphone", "phone prices", "low cost phone"],
    "Food affordability pressure": ["maize flour", "unga", "food prices", "flour prices", "maize prices"],
    "Fuel and logistics inflation": ["fuel prices", "petrol", "diesel", "transport cost", "matatu fare"],
    "Water access stress": ["water shortage", "water rationing", "borehole", "drought water"],
    "Youth jobs pressure": ["jobs", "employment", "hiring", "job search", "youth unemployment"],
    "Housing affordability pressure": ["rent", "housing", "apartment", "bedsitter", "house prices"],
}

STOPWORDS = {"in", "the", "and", "near", "me", "kenya", "for", "a", "to", "of"}


def topic_embedding(topic: str) -> dict[str, float]:
    tokens = [token for token in _tokens(topic) if token not in STOPWORDS]
    counts = Counter(tokens)
    norm = math.sqrt(sum(value * value for value in counts.values())) or 1.0
    return {token: value / norm for token, value in counts.items()}


def semantic_similarity(left: str, right: str) -> float:
    left_vec = topic_embedding(left)
    right_vec = topic_embedding(right)
    shared = set(left_vec) & set(right_vec)
    cosine = sum(left_vec[token] * right_vec[token] for token in shared)
    sequence = SequenceMatcher(None, left.lower(), right.lower()).ratio()
    synonym_boost = 0.25 if canonical_theme(left) == canonical_theme(right) else 0.0
    return min(1.0, cosine * 0.55 + sequence * 0.30 + synonym_boost)


def canonical_theme(topic: str) -> str:
    text = topic.lower()
    for theme, phrases in THEME_SYNONYMS.items():
        if any(phrase in text for phrase in phrases):
            return theme
    return " ".join(_tokens(topic)[:4]).title() or "General Kenya Signal"


def cluster_related_topics(signals: list[dict[str, Any]], threshold: float = 0.62) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for signal in signals:
        topic = str(signal.get("signal_topic") or signal.get("topic") or "")
        theme = canonical_theme(topic)
        placed = False
        for cluster in clusters:
            if cluster["semantic_cluster"] == theme or semantic_similarity(topic, cluster["representative_topic"]) >= threshold:
                cluster["topics"].append(topic)
                cluster["signals"].append(signal)
                placed = True
                break
        if not placed:
            clusters.append({"semantic_cluster": theme, "representative_topic": topic, "topics": [topic], "signals": [signal]})
    return clusters


def enrich_with_semantics(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters = cluster_related_topics(signals)
    output: list[dict[str, Any]] = []
    for cluster in clusters:
        latent_theme = detect_latent_theme(cluster["topics"])
        for signal in cluster["signals"]:
            enriched = dict(signal)
            enriched["semantic_cluster"] = cluster["semantic_cluster"]
            enriched["latent_theme"] = latent_theme
            enriched["related_topics"] = sorted(set(cluster["topics"]))[:8]
            output.append(enriched)
    return output


def detect_latent_theme(topics: list[str]) -> str:
    text = " ".join(topics).lower()
    if any(word in text for word in ["price", "prices", "cheap", "affordable", "cost", "rent", "fuel", "unga"]):
        return "affordability pressure"
    if any(word in text for word in ["shortage", "drought", "water", "hospital", "clinic"]):
        return "service or supply stress"
    if any(word in text for word in ["job", "employment", "hiring"]):
        return "livelihood and employment pressure"
    if any(word in text for word in ["smartphone", "digital", "loan", "internet"]):
        return "digital adoption and consumer access"
    return "emerging demand pattern"


def merge_synonymous_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters = cluster_related_topics(signals)
    merged: list[dict[str, Any]] = []
    for cluster in clusters:
        strongest = max(cluster["signals"], key=lambda item: float(item.get("confidence_score", item.get("priority_score", 0))))
        item = dict(strongest)
        item["signal_topic"] = cluster["semantic_cluster"]
        item["related_topics"] = sorted(set(cluster["topics"]))[:8]
        item["latent_theme"] = detect_latent_theme(cluster["topics"])
        merged.append(item)
    return merged


def _tokens(topic: str) -> list[str]:
    cleaned = "".join(char.lower() if char.isalnum() else " " for char in str(topic))
    return [token for token in cleaned.split() if token]

def cluster_related_records(records: list[dict[str, Any]], threshold: float = 0.62) -> dict[str, list[dict[str, Any]]]:
    """Group normalized source records by semantic theme."""
    clusters = cluster_related_topics(records, threshold=threshold)
    return {cluster["semantic_cluster"]: list(cluster["signals"]) for cluster in clusters}


def detect_latent_themes(records: list[dict[str, Any]] | list[str]) -> list[str]:
    """Return compact latent themes represented by records or topic strings."""
    topics: list[str] = []
    for item in records:
        if isinstance(item, dict):
            topics.append(str(item.get("signal_topic") or item.get("topic") or ""))
        else:
            topics.append(str(item))
    themes = {detect_latent_theme([topic]) for topic in topics if topic}
    if len(topics) > 1:
        themes.add(detect_latent_theme(topics))
    return sorted(theme for theme in themes if theme)
