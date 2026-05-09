"""Trainable preference model for the Signal prototype."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .research import (
    PUBLICATION_NOTES,
    cge_sam_shock,
    policy_signal,
    sam_account_for_category,
)
from .schemas import FeatureContribution, PreferenceExample, PreferencePrediction, PreferenceRequest


CATEGORICAL_FEATURES = ["user_id", "category"]
NUMERIC_FEATURES = ["price", "rating", "popularity"]


class PreferenceModel:
    """A lightweight classifier that scores whether a user will prefer an item."""

    def __init__(self, pipeline: Pipeline | None = None) -> None:
        self.pipeline = pipeline or self._build_pipeline()

    def train(self, examples: Iterable[PreferenceExample]) -> "PreferenceModel":
        frame = _examples_to_frame(examples)
        if frame.empty:
            raise ValueError("at least one training example is required")
        if frame["label"].nunique() < 2:
            raise ValueError("training examples must include both positive and negative labels")

        self.pipeline.fit(frame[CATEGORICAL_FEATURES + NUMERIC_FEATURES], frame["label"])
        return self

    def predict(self, request: PreferenceRequest) -> PreferencePrediction:
        frame = _requests_to_frame([request])
        probability = float(self.pipeline.predict_proba(frame)[0][1])
        score = round(probability, 4)
        preferred = probability >= 0.5
        return PreferencePrediction(
            item_id=request.item_id,
            score=score,
            preferred=preferred,
            drivers=tuple(self.explain(request)),
            policy_signal=policy_signal(score, preferred),
            cge_sam_account=sam_account_for_category(request.category),
            cge_sam_shock=cge_sam_shock(score),
            publication_notes=PUBLICATION_NOTES,
        )

    def predict_many(self, requests: Iterable[PreferenceRequest]) -> list[PreferencePrediction]:
        request_list = list(requests)
        if not request_list:
            return []

        frame = _requests_to_frame(request_list)
        probabilities = self.pipeline.predict_proba(frame)[:, 1]
        predictions = []
        for request, probability in zip(request_list, probabilities, strict=True):
            score = round(float(probability), 4)
            preferred = float(probability) >= 0.5
            predictions.append(
                PreferencePrediction(
                    item_id=request.item_id,
                    score=score,
                    preferred=preferred,
                    drivers=tuple(self.explain(request)),
                    policy_signal=policy_signal(score, preferred),
                    cge_sam_account=sam_account_for_category(request.category),
                    cge_sam_shock=cge_sam_shock(score),
                    publication_notes=PUBLICATION_NOTES,
                )
            )
        return predictions

    def explain(self, request: PreferenceRequest, top_n: int = 5) -> list[FeatureContribution]:
        """Return the largest coefficient-weighted feature drivers for a request."""

        frame = _requests_to_frame([request])
        preprocessor = self.pipeline.named_steps["preprocessor"]
        classifier = self.pipeline.named_steps["classifier"]
        transformed = preprocessor.transform(frame)
        row = transformed.toarray()[0] if hasattr(transformed, "toarray") else transformed[0]
        feature_names = preprocessor.get_feature_names_out()
        contributions = row * classifier.coef_[0]

        ranked = sorted(
            zip(feature_names, contributions, strict=True),
            key=lambda item: abs(float(item[1])),
            reverse=True,
        )
        return [
            FeatureContribution(
                feature=_clean_feature_name(name),
                value=_feature_value(name, request),
                contribution=round(float(contribution), 4),
                direction="supports_preference" if float(contribution) >= 0 else "reduces_preference",
            )
            for name, contribution in ranked[:top_n]
        ]

    def evaluate(self, examples: Iterable[PreferenceExample]) -> dict[str, float]:
        frame = _examples_to_frame(examples)
        if frame.empty:
            raise ValueError("at least one evaluation example is required")

        features = frame[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
        labels = frame["label"]
        predictions = self.pipeline.predict(features)
        probabilities = self.pipeline.predict_proba(features)[:, 1]
        metrics = {"accuracy": round(float(accuracy_score(labels, predictions)), 4)}
        metrics["n_examples"] = float(len(frame))
        metrics["positive_rate"] = round(float(labels.mean()), 4)
        if labels.nunique() > 1:
            metrics["roc_auc"] = round(float(roc_auc_score(labels, probabilities)), 4)
        return metrics

    def save(self, path: str | Path) -> None:
        model_path = Path(path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, model_path)

    @classmethod
    def load(cls, path: str | Path) -> "PreferenceModel":
        return cls(pipeline=joblib.load(path))

    @staticmethod
    def _build_pipeline() -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
                ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ]
        )
        return Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        )


def _examples_to_frame(examples: Iterable[PreferenceExample]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": example.user_id,
                "item_id": example.item_id,
                "category": example.category,
                "price": example.price,
                "rating": example.rating,
                "popularity": example.popularity,
                "label": example.label,
            }
            for example in examples
        ]
    )


def _requests_to_frame(requests: Iterable[PreferenceRequest]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": request.user_id,
                "item_id": request.item_id,
                "category": request.category,
                "price": request.price,
                "rating": request.rating,
                "popularity": request.popularity,
            }
            for request in requests
        ]
    )


def _clean_feature_name(name: str) -> str:
    cleaned = name.split("__", maxsplit=1)[-1]
    if cleaned.startswith("user_id_"):
        return "user_id"
    if cleaned.startswith("category_"):
        return "category"
    return cleaned


def _feature_value(name: str, request: PreferenceRequest) -> str:
    cleaned = name.split("__", maxsplit=1)[-1]
    if cleaned.startswith("user_id_"):
        return request.user_id
    if cleaned.startswith("category_"):
        return request.category
    return str(getattr(request, cleaned))
