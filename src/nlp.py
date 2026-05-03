"""Learned NLP utilities for anonymized behavioral signal text."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class SignalNLPModel:
    """Supervised NLP model for sentiment, intent, urgency, dissatisfaction, and topics."""

    max_features: int = 300
    random_state: int = 42

    def __post_init__(self) -> None:
        self.vectorizer = TfidfVectorizer(max_features=self.max_features, ngram_range=(1, 2))
        self.sentiment_model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        self.intent_model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        self.urgency_model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        self.dissatisfaction_model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        self.topic_model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        self.is_trained = False

    def fit(self, frame: pd.DataFrame) -> "SignalNLPModel":
        texts = _texts(frame["text"])
        matrix = self.vectorizer.fit_transform(texts)
        self.sentiment_model.fit(matrix, frame["sentiment_label"])
        self.intent_model.fit(matrix, frame["purchase_intent_label"])
        self.urgency_model.fit(matrix, frame["urgency_label"])
        self.dissatisfaction_model.fit(matrix, frame["dissatisfaction_label"])
        self.topic_model.fit(matrix, frame["topic_label"])
        self.is_trained = True
        return self

    def transform(self, texts: Iterable[str]) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("SignalNLPModel must be fitted before transform")

        matrix = self.vectorizer.transform(_texts(texts))
        topic_probabilities = self.topic_model.predict_proba(matrix)
        topic_labels = self.topic_model.predict(matrix)
        return pd.DataFrame(
            {
                "sentiment_score": _class_probability(self.sentiment_model, matrix, positive_class=1),
                "purchase_intent_score": _class_probability(self.intent_model, matrix, positive_class=1),
                "urgency_score": _class_probability(self.urgency_model, matrix, positive_class=1),
                "dissatisfaction_score": _class_probability(self.dissatisfaction_model, matrix, positive_class=1),
                "nlp_topic": topic_labels,
                "topic_confidence": topic_probabilities.max(axis=1),
            }
        )


def _texts(values: Iterable[str]) -> list[str]:
    return [str(value) for value in values]


def _class_probability(model: LogisticRegression, matrix, positive_class: int) -> list[float]:
    probabilities = model.predict_proba(matrix)
    classes = list(model.classes_)
    if positive_class not in classes:
        return [0.0 for _ in range(probabilities.shape[0])]
    class_index = classes.index(positive_class)
    return [round(float(value), 4) for value in probabilities[:, class_index]]
