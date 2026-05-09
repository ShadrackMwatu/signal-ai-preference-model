"""Train the primary Signal AI/ML demand model and persist metadata locally."""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data.synthetic.generate_synthetic_signal_data import DEMAND_CLASSES, generate_synthetic_signal_data


ROOT_DIR = Path(__file__).resolve().parent
TRAINING_DATA_PATH = ROOT_DIR / "data" / "training" / "signal_training_data.csv"
MODEL_PATH = ROOT_DIR / "models" / "model.pkl"
METADATA_PATH = ROOT_DIR / "models" / "metadata.json"
MODEL_VERSIONS_DIR = ROOT_DIR / "models" / "versions"

BASE_FEATURE_COLUMNS = [
    "likes",
    "comments",
    "shares",
    "searches",
    "engagement_intensity",
    "purchase_intent_score",
    "trend_growth",
    "sentiment_score",
    "urgency_score",
    "repetition_score",
    "location_relevance",
    "price_sensitivity",
    "noise_score",
]
DERIVED_FEATURE_COLUMNS = [
    "mentions_count",
    "comments_count",
    "shares_count",
    "likes_count",
    "searches_count",
    "engagement_rate",
    "weighted_engagement_score",
    "trend_momentum",
    "unmet_need_signal",
    "opportunity_index",
]
FEATURE_COLUMNS = BASE_FEATURE_COLUMNS + DERIVED_FEATURE_COLUMNS
REQUIRED_COLUMNS = [
    "topic",
    "county",
    "time_period",
    "likes",
    "comments",
    "shares",
    "searches",
    "engagement_intensity",
    "purchase_intent_score",
    "trend_growth",
    "sentiment_score",
    "urgency_score",
    "repetition_score",
    "location_relevance",
    "price_sensitivity",
    "noise_score",
    "demand_class",
    "opportunity_label",
    "unmet_demand_flag",
    "emerging_trend_flag",
]
TARGET_COLUMN = "demand_class"


@dataclass
class TrainingResult:
    model_path: str
    metadata_path: str
    model_version: str
    training_rows: int
    train_accuracy: float
    test_accuracy: float
    cross_validation_score: float | None

    @property
    def accuracy_score(self) -> float:
        return self.test_accuracy


def generate_training_data(
    output_path: str | Path = TRAINING_DATA_PATH,
    n_rows: int = 1800,
    random_state: int = 42,
) -> pd.DataFrame:
    """Backward-compatible wrapper around the phase-2 synthetic generator."""

    return generate_synthetic_signal_data(output_path=output_path, n_rows=n_rows, random_state=random_state)


def load_training_data(path: str | Path = TRAINING_DATA_PATH) -> pd.DataFrame:
    data_path = Path(path)
    if not data_path.exists():
        return generate_synthetic_signal_data(data_path)
    frame = pd.read_csv(data_path)
    _validate_training_frame(frame)
    return frame


def prepare_training_frame(frame: pd.DataFrame) -> pd.DataFrame:
    prepared = frame.copy()
    _validate_training_frame(prepared)

    numeric_columns = [
        "likes",
        "comments",
        "shares",
        "searches",
        "engagement_intensity",
        "purchase_intent_score",
        "trend_growth",
        "sentiment_score",
        "urgency_score",
        "repetition_score",
        "location_relevance",
        "price_sensitivity",
        "noise_score",
        "unmet_demand_flag",
        "emerging_trend_flag",
    ]
    for column in numeric_columns:
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    prepared["likes"] = prepared["likes"].fillna(prepared["likes"].median())
    prepared["comments"] = prepared["comments"].fillna(prepared["comments"].median())
    prepared["shares"] = prepared["shares"].fillna(prepared["shares"].median())
    prepared["searches"] = prepared["searches"].fillna(prepared["searches"].median())

    for column in [
        "engagement_intensity",
        "purchase_intent_score",
        "sentiment_score",
        "urgency_score",
        "repetition_score",
        "location_relevance",
        "price_sensitivity",
        "noise_score",
    ]:
        prepared[column] = prepared[column].fillna(prepared[column].median()).clip(0, 1)

    prepared["trend_growth"] = prepared["trend_growth"].fillna(prepared["trend_growth"].median()).clip(-1, 1)
    prepared["unmet_demand_flag"] = prepared["unmet_demand_flag"].fillna(0).clip(0, 1).round().astype(int)
    prepared["emerging_trend_flag"] = prepared["emerging_trend_flag"].fillna(0).clip(0, 1).round().astype(int)

    total_engagement = prepared["likes"] + prepared["comments"] + prepared["shares"] + prepared["searches"]
    prepared["mentions_count"] = prepared["comments"] + (prepared["shares"] * 0.5)
    prepared["comments_count"] = prepared["comments"]
    prepared["shares_count"] = prepared["shares"]
    prepared["likes_count"] = prepared["likes"]
    prepared["searches_count"] = prepared["searches"]
    prepared["engagement_rate"] = np.clip(total_engagement / np.maximum(total_engagement + 120, 1), 0, 1)
    prepared["weighted_engagement_score"] = np.clip(
        (
            prepared["likes"]
            + prepared["comments"] * 1.8
            + prepared["shares"] * 2.4
            + prepared["searches"] * 1.6
            + prepared["mentions_count"]
        )
        / 100,
        0,
        12,
    )
    prepared["trend_momentum"] = np.clip((prepared["trend_growth"] * 0.65) + (prepared["urgency_score"] * 0.35), 0, 1)
    prepared["unmet_need_signal"] = np.clip(
        (prepared["urgency_score"] * 0.4)
        + (prepared["price_sensitivity"] * 0.18)
        + ((1 - prepared["engagement_intensity"]) * 0.16)
        + (prepared["purchase_intent_score"] * 0.18)
        - (prepared["noise_score"] * 0.12),
        0,
        1,
    )
    prepared["opportunity_index"] = np.clip(
        (prepared["engagement_intensity"] * 0.2)
        + (prepared["purchase_intent_score"] * 0.22)
        + (prepared["trend_growth"].clip(lower=0) * 0.18)
        + (prepared["urgency_score"] * 0.14)
        + (prepared["repetition_score"] * 0.08)
        + (prepared["location_relevance"] * 0.08)
        + (prepared["unmet_need_signal"] * 0.16)
        - (prepared["noise_score"] * 0.1),
        0,
        1,
    )
    prepared[TARGET_COLUMN] = prepared[TARGET_COLUMN].fillna("Moderate Demand").astype(str)
    return prepared


def train_signal_model(
    data_path: str | Path = TRAINING_DATA_PATH,
    model_path: str | Path = MODEL_PATH,
    metadata_path: str | Path = METADATA_PATH,
    random_state: int = 42,
) -> TrainingResult:
    """Train the primary demand-classification pipeline and companion classifiers."""

    raw = load_training_data(data_path)
    frame = prepare_training_frame(raw)

    if not _has_sufficient_class_balance(frame[TARGET_COLUMN]):
        raw = generate_synthetic_signal_data(data_path, random_state=random_state)
        frame = prepare_training_frame(raw)

    x = frame[FEATURE_COLUMNS]
    y = frame[TARGET_COLUMN]
    x_train, x_test, y_train, y_test, use_holdout = _safe_train_test_split(x, y, random_state=random_state)

    primary_pipeline = _build_classifier_pipeline(random_state)
    primary_pipeline.fit(x_train, y_train)
    train_accuracy = float(accuracy_score(y_train, primary_pipeline.predict(x_train)))
    test_accuracy = float(accuracy_score(y_test, primary_pipeline.predict(x_test))) if use_holdout else train_accuracy

    cv_score = _safe_cross_validation(primary_pipeline, x, y)

    unmet_pipeline = _build_classifier_pipeline(random_state + 1)
    unmet_pipeline.fit(x, frame["unmet_demand_flag"])

    emerging_pipeline = _build_classifier_pipeline(random_state + 2)
    emerging_pipeline.fit(x, frame["emerging_trend_flag"])

    model_version = _next_model_version()
    artifact = {
        "model": primary_pipeline,
        "unmet_model": unmet_pipeline,
        "emerging_model": emerging_pipeline,
        "feature_columns": FEATURE_COLUMNS,
        "base_feature_columns": BASE_FEATURE_COLUMNS,
        "derived_feature_columns": DERIVED_FEATURE_COLUMNS,
        "class_labels": DEMAND_CLASSES,
        "target_column": TARGET_COLUMN,
        "model_version": model_version,
        "trained_at": datetime.now(UTC).isoformat(),
    }

    model_file = Path(model_path)
    model_file.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_file)

    metadata = {
        "model_version": model_version,
        "training_date": artifact["trained_at"],
        "number_of_rows": len(frame),
        "features_used": FEATURE_COLUMNS,
        "target_variable": TARGET_COLUMN,
        "model_type": "RandomForestClassifier pipeline",
        "train_accuracy": round(train_accuracy, 4),
        "test_accuracy": round(test_accuracy, 4),
        "accuracy_score": round(test_accuracy, 4),
        "cross_validation_score": None if cv_score is None else round(cv_score, 4),
        "package_versions": {
            "numpy": version("numpy"),
            "pandas": version("pandas"),
            "scikit-learn": version("scikit-learn"),
            "joblib": version("joblib"),
        },
        "artifact_path": str(model_file),
        "data_path": str(Path(data_path)),
    }

    metadata_file = Path(metadata_path)
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    _write_versioned_artifacts(model_file, metadata_file, model_version)

    return TrainingResult(
        model_path=str(model_file),
        metadata_path=str(metadata_file),
        model_version=model_version,
        training_rows=len(frame),
        train_accuracy=round(train_accuracy, 4),
        test_accuracy=round(test_accuracy, 4),
        cross_validation_score=None if cv_score is None else round(cv_score, 4),
    )


def _build_classifier_pipeline(random_state: int) -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                FEATURE_COLUMNS,
            )
        ]
    )
    model = RandomForestClassifier(
        n_estimators=240,
        min_samples_leaf=2,
        random_state=random_state,
        class_weight="balanced_subsample",
    )
    return Pipeline(steps=[("preprocess", preprocessing), ("model", model)])


def _safe_train_test_split(
    x: pd.DataFrame,
    y: pd.Series,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, bool]:
    minimum_class_size = int(y.value_counts().min()) if not y.empty else 0
    use_holdout = len(x) >= 18 and y.nunique() >= 2 and minimum_class_size >= 2
    if use_holdout:
        return (*train_test_split(x, y, test_size=0.2, random_state=random_state, stratify=y), True)
    return x, x, y, y, False


def _safe_cross_validation(model: Pipeline, x: pd.DataFrame, y: pd.Series) -> float | None:
    if len(x) < 24 or y.nunique() < 2:
        return None
    minimum_class_size = int(y.value_counts().min())
    folds = min(5, minimum_class_size)
    if folds < 2:
        return None
    try:
        return float(cross_val_score(model, x, y, cv=folds, scoring="accuracy").mean())
    except Exception:
        return None


def _write_versioned_artifacts(model_file: Path, metadata_file: Path, model_version: str) -> None:
    version_dir = MODEL_VERSIONS_DIR / model_version
    version_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(model_file, version_dir / "model.pkl")
    shutil.copy2(metadata_file, version_dir / "metadata.json")


def _next_model_version() -> str:
    MODEL_VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    existing = []
    for path in MODEL_VERSIONS_DIR.iterdir():
        if path.is_dir() and path.name.startswith("v") and path.name[1:].isdigit():
            existing.append(int(path.name[1:]))
    return f"v{max(existing, default=0) + 1}"


def _validate_training_frame(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Training data is missing required columns: {', '.join(missing)}")


def _has_sufficient_class_balance(target: pd.Series) -> bool:
    counts = target.astype(str).value_counts()
    return counts.size >= 3 and int(counts.min()) >= 2


def main() -> None:
    result = train_signal_model()
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
