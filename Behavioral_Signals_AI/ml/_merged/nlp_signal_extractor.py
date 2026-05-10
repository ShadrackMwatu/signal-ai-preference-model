"""NLP signal extraction with optional spaCy/transformer support and TF-IDF fallback."""

from __future__ import annotations

import re
import os
from functools import lru_cache
from typing import Iterable, Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


POSITIVE_TERMS = {"reliable", "quality", "trusted", "available", "fast", "saves", "good"}
NEGATIVE_TERMS = {"delay", "delays", "poor", "expensive", "shortage", "complaint", "complaints"}
INTENT_TERMS = {"buy", "order", "purchase", "supplier", "suppliers", "compare", "quote"}
URGENCY_TERMS = {"urgent", "now", "today", "immediate", "fast", "asap"}
TOPIC_TERMS = {
    "agriculture": {"seed", "fertilizer", "farm", "harvest"},
    "clean_energy": {"solar", "battery", "power", "repair"},
    "digital_services": {"payments", "dashboard", "analytics", "mobile"},
    "transport": {"delivery", "route", "parcel", "logistics"},
}


def extract_text_signals(texts: Iterable[str]) -> pd.DataFrame:
    """Extract sentiment, urgency, intent, complaint, and topic signals from text."""

    return pd.DataFrame([_extract_one(text) for text in texts])


def build_text_embeddings(texts: Iterable[str]) -> dict[str, Any]:
    """Build text embeddings with sentence-transformers when available, otherwise TF-IDF."""

    normalized = [preprocess_text(text) for text in texts]
    transformer = _sentence_transformer()
    if transformer is not None:
        return {
            "embeddings": transformer.encode(normalized).tolist(),
            "embedding_source": "sentence-transformers",
        }
    vectorizer = TfidfVectorizer(max_features=128)
    matrix = vectorizer.fit_transform(normalized)
    return {
        "embeddings": matrix.toarray().tolist(),
        "embedding_source": "tf-idf fallback",
        "vocabulary": vectorizer.get_feature_names_out().tolist(),
    }


def preprocess_text(text: str) -> str:
    """Normalize text using spaCy if available, otherwise a lightweight regex tokenizer."""

    nlp = _spacy_model()
    if nlp is not None:
        doc = nlp(str(text))
        return " ".join((token.lemma_ or token.text).lower() for token in doc if not token.is_space and not token.is_punct)
    return " ".join(re.findall(r"[a-zA-Z_]+", str(text).lower()))


def optional_deep_learning_status() -> dict[str, bool]:
    """Report optional ML library availability without making imports mandatory."""

    return {
        "torch_available": _can_import("torch"),
        "tensorflow_available": _can_import("tensorflow"),
        "transformers_available": _can_import("transformers"),
        "sentence_transformers_available": _sentence_transformer() is not None,
        "spacy_available": _spacy_model() is not None,
    }


def _extract_one(text: str) -> dict[str, Any]:
    processed = preprocess_text(text)
    tokens = set(processed.split())
    positive = len(tokens.intersection(POSITIVE_TERMS))
    negative = len(tokens.intersection(NEGATIVE_TERMS))
    intent = len(tokens.intersection(INTENT_TERMS))
    urgency = len(tokens.intersection(URGENCY_TERMS))
    topic_scores = {topic: len(tokens.intersection(terms)) for topic, terms in TOPIC_TERMS.items()}
    topic = max(topic_scores, key=topic_scores.get)
    complaint = len(tokens.intersection(NEGATIVE_TERMS))
    return {
        "clean_text": processed,
        "sentiment_score": _bounded((positive + 1) / (positive + negative + 2)),
        "purchase_intent_score": _bounded(intent / 4),
        "urgency_score": _bounded(urgency / 3),
        "complaint_score": _bounded(complaint / 4),
        "topic": topic,
        "topic_confidence": _bounded(topic_scores[topic] / 4),
        "nlp_source": "spacy" if _spacy_model() is not None else "regex fallback",
    }


@lru_cache(maxsize=1)
def _spacy_model() -> Any | None:
    try:
        import spacy

        try:
            return spacy.load("en_core_web_sm")
        except Exception:
            return spacy.blank("en")
    except Exception:
        return None


@lru_cache(maxsize=1)
def _sentence_transformer() -> Any | None:
    if os.environ.get("SIGNAL_ENABLE_SENTENCE_TRANSFORMERS") != "1":
        return None
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return None


def _can_import(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except Exception:
        return False


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 4)
