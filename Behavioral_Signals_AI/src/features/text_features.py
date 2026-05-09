"""Rule-based NLP feature extraction with future model-upgrade seams."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import pandas as pd


POSITIVE_TERMS = {"reliable", "positive", "saves", "ready", "trusted", "quality", "available"}
NEGATIVE_TERMS = {"complaints", "delay", "delays", "unmet", "poor", "expensive", "shortage"}
INTENT_TERMS = {"buy", "supplier", "suppliers", "order", "purchase", "compare", "ready"}
COMPLAINT_TERMS = {"complaints", "delay", "delays", "unmet", "shortage", "poor"}
URGENCY_TERMS = {"ready", "urgent", "now", "fast", "immediate", "delays"}
TOPIC_TERMS = {
    "agri_inputs": {"seed", "fertilizer", "harvest", "farm"},
    "clean_energy": {"solar", "battery", "power", "repair"},
    "digital_services": {"payments", "analytics", "dashboard", "mobile"},
    "retail": {"prices", "availability", "delivery", "product"},
    "transport": {"route", "parcel", "tracking", "mile"},
}


@dataclass
class TextFeatureExtractor:
    """Version-1 keyword NLP extractor; replace internals later with transformer models."""

    def transform(self, texts: Iterable[str]) -> pd.DataFrame:
        return pd.DataFrame([extract_text_features(text) for text in texts])


def extract_text_features(text: str) -> dict[str, object]:
    """Extract sentiment, intent, complaint, urgency, and topic keywords."""

    tokens = _tokens(text)
    token_set = set(tokens)
    positive_hits = len(token_set.intersection(POSITIVE_TERMS))
    negative_hits = len(token_set.intersection(NEGATIVE_TERMS))
    intent_hits = len(token_set.intersection(INTENT_TERMS))
    complaint_hits = len(token_set.intersection(COMPLAINT_TERMS))
    urgency_hits = len(token_set.intersection(URGENCY_TERMS))
    topic_scores = {
        topic: len(token_set.intersection(terms))
        for topic, terms in TOPIC_TERMS.items()
    }
    topic_keywords = sorted(
        {token for terms in TOPIC_TERMS.values() for token in token_set.intersection(terms)}
    )
    best_topic = max(topic_scores, key=topic_scores.get)
    topic_confidence = _bounded(topic_scores[best_topic] / 4)

    return {
        "sentiment_score": _bounded((positive_hits + 1) / (positive_hits + negative_hits + 2)),
        "purchase_intent_score": _bounded(intent_hits / 4),
        "complaint_score": _bounded(complaint_hits / 4),
        "urgency_score": _bounded(urgency_hits / 3),
        "topic_keywords": ",".join(topic_keywords),
        "nlp_topic": best_topic,
        "topic_confidence": topic_confidence,
    }


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z_]+", str(text).lower())


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 4)
