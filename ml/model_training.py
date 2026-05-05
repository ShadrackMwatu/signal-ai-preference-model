"""Scikit-learn-first model training utilities for Signal."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from .feature_engineering import build_behavioral_features, select_numeric_features
from .model_evaluation import evaluate_classification, evaluate_regression
from .model_registry import ModelRegistry


DEFAULT_MODEL_DIR = Path("models_ml") / "trained_models"


def train_demand_classifier(
    frame: pd.DataFrame,
    target_column: str = "demand_class",
    feature_columns: list[str] | None = None,
    model_name: str = "signal_demand_classifier",
    output_dir: str | Path = DEFAULT_MODEL_DIR,
    dataset_used: str = "in-memory",
    algorithm: str = "random_forest",
    registry: ModelRegistry | None = None,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a demand-signal classifier with RandomForest or LogisticRegression."""

    features = build_behavioral_features(frame)
    columns = feature_columns or select_numeric_features(features)
    x = features[columns]
    y = features[target_column]
    test_size = 0.25
    expected_test_rows = max(1, int(round(len(y) * test_size)))
    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 and expected_test_rows >= y.nunique() else None
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    model = (
        LogisticRegression(max_iter=1000, random_state=random_state)
        if algorithm == "logistic_regression"
        else RandomForestClassifier(n_estimators=100, min_samples_leaf=2, random_state=random_state)
    )
    model.fit(x_train, y_train)
    metrics = evaluate_classification(y_test, model.predict(x_test))
    path = _save_model(model, model_name, output_dir)
    registry = registry or ModelRegistry()
    record = registry.register_model(
        model_name=model_name,
        model_type=f"classification:{algorithm}",
        dataset_used=dataset_used,
        performance={"accuracy": metrics["accuracy"]},
        file_path=str(path),
        notes="Default scikit-learn Signal demand classifier.",
    )
    return {
        "model": model,
        "model_path": str(path),
        "feature_columns": columns,
        "metrics": metrics,
        "registry_record": record,
        "prediction_source": "trained ML model",
    }


def train_regression_model(
    frame: pd.DataFrame,
    target_column: str,
    feature_columns: list[str] | None = None,
    model_name: str = "signal_regression_model",
    output_dir: str | Path = DEFAULT_MODEL_DIR,
    dataset_used: str = "in-memory",
    registry: ModelRegistry | None = None,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a RandomForestRegressor for aggregate demand or opportunity scores."""

    features = build_behavioral_features(frame)
    columns = feature_columns or select_numeric_features(features)
    x_train, x_test, y_train, y_test = train_test_split(
        features[columns],
        features[target_column],
        test_size=0.25,
        random_state=random_state,
    )
    model = RandomForestRegressor(n_estimators=100, min_samples_leaf=2, random_state=random_state)
    model.fit(x_train, y_train)
    metrics = evaluate_regression(y_test, model.predict(x_test))
    path = _save_model(model, model_name, output_dir)
    registry = registry or ModelRegistry()
    record = registry.register_model(
        model_name=model_name,
        model_type="regression:random_forest",
        dataset_used=dataset_used,
        performance=metrics,
        file_path=str(path),
        notes="Default scikit-learn Signal regression model.",
    )
    return {
        "model": model,
        "model_path": str(path),
        "feature_columns": columns,
        "metrics": metrics,
        "registry_record": record,
        "prediction_source": "trained ML model",
    }


def train_county_topic_clusterer(
    frame: pd.DataFrame,
    feature_columns: list[str] | None = None,
    n_clusters: int = 3,
    random_state: int = 42,
) -> dict[str, Any]:
    """Cluster counties, topics, households, or aggregate demand segments with KMeans."""

    features = build_behavioral_features(frame)
    columns = feature_columns or select_numeric_features(features)
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(features[columns])
    return {
        "model": model,
        "labels": labels,
        "feature_columns": columns,
        "prediction_source": "trained ML model",
    }


def load_trained_model(path: str | Path) -> Any:
    """Load a previously saved scikit-learn model."""

    return joblib.load(path)


def _save_model(model: Any, model_name: str, output_dir: str | Path) -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{model_name}.joblib"
    joblib.dump(model, path)
    return path
