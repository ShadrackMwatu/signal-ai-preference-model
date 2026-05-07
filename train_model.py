"""Train the primary Signal AI/ML demand model and persist metadata locally."""

from __future__ import annotations

import json
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


ROOT_DIR = Path(__file__).resolve().parent
TRAINING_DATA_PATH = ROOT_DIR / "data" / "training" / "signal_training_data.csv"
MODEL_PATH = ROOT_DIR / "models" / "model.pkl"
METADATA_PATH = ROOT_DIR / "models" / "metadata.json"

PRIMARY_FEATURE_COLUMNS = [
    "engagement_intensity",
    "mentions_count",
    "comments_count",
    "shares_count",
    "likes_count",
    "searches_count",
    "sentiment_score",
    "urgency_score",
    "trend_growth",
    "repetition_score",
    "location_relevance",
    "price_sensitivity",
    "noise_score",
    "engagement_rate",
    "weighted_engagement_score",
    "trend_momentum",
    "unmet_need_signal",
    "opportunity_index",
]
REQUIRED_COLUMNS = PRIMARY_FEATURE_COLUMNS + [
    "county",
    "topic",
    "time_period",
    "demand_classification",
    "opportunity_score",
    "unmet_demand_flag",
    "emerging_trend_flag",
]
DEMAND_CLASS_ORDER = ["Low Demand", "Moderate Demand", "High Demand"]


@dataclass
class TrainingResult:
    model_path: str
    metadata_path: str
    training_rows: int
    accuracy_score: float
    cross_validation_score: float | None


def generate_training_data(
    output_path: str | Path = TRAINING_DATA_PATH,
    n_rows: int = 1500,
    random_state: int = 42,
) -> pd.DataFrame:
    """Create a synthetic, privacy-safe training dataset for Signal."""

    rng = np.random.default_rng(random_state)
    counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Machakos", "Kiambu", "Turkana"]
    topics = ["retail", "food", "finance", "health", "mobility", "agriculture", "education"]
    periods = [f"2026-Q{quarter}" for quarter in range(1, 5)]

    rows: list[dict[str, Any]] = []
    for _ in range(n_rows):
        county = str(rng.choice(counties))
        topic = str(rng.choice(topics))
        time_period = str(rng.choice(periods))

        likes_count = int(rng.poisson(40))
        comments_count = int(rng.poisson(18))
        shares_count = int(rng.poisson(10))
        searches_count = int(rng.poisson(55))
        mentions_count = int(rng.poisson(14))
        views_count = int(max(80, rng.poisson(280)))

        engagement_intensity = np.clip(
            0.28
            + likes_count / 420
            + comments_count / 180
            + shares_count / 130
            + searches_count / 360
            + rng.normal(0, 0.06),
            0,
            1,
        )
        sentiment_score = float(np.clip(rng.normal(0.15 + engagement_intensity * 0.55, 0.16), -1, 1))
        urgency_score = float(np.clip(rng.normal(searches_count / 140 + shares_count / 90, 0.12), 0, 1))
        trend_growth = float(np.clip(rng.normal(engagement_intensity * 0.7, 0.18), -0.2, 1))
        repetition_score = float(np.clip(rng.normal(searches_count / max(likes_count + comments_count, 1), 0.12), 0, 1))
        location_relevance = float(np.clip(rng.normal(0.55 if county != "Turkana" else 0.48, 0.12), 0, 1))
        price_sensitivity = float(np.clip(rng.normal(0.55 - sentiment_score * 0.15, 0.18), 0, 1))
        noise_score = float(np.clip(rng.normal(0.35 + abs(sentiment_score) * 0.1, 0.14), 0, 1))

        engagement_rate = float(np.clip((likes_count + comments_count + shares_count + searches_count) / views_count, 0, 1.5))
        weighted_engagement_score = float(
            np.clip(
                (
                    likes_count
                    + comments_count * 1.8
                    + shares_count * 2.4
                    + searches_count * 1.6
                    + mentions_count * 1.1
                )
                / 100,
                0,
                10,
            )
        )
        trend_momentum = float(np.clip((trend_growth * 0.65) + (urgency_score * 0.35), 0, 1))
        unmet_need_signal = float(np.clip((urgency_score * 0.45) + (price_sensitivity * 0.2) - (noise_score * 0.15), 0, 1))
        opportunity_index = float(
            np.clip(
                (engagement_intensity * 0.22)
                + (max(sentiment_score, 0) * 0.12)
                + (trend_growth * 0.2)
                + (urgency_score * 0.16)
                + (unmet_need_signal * 0.16)
                + (location_relevance * 0.08)
                - (noise_score * 0.08),
                0,
                1,
            )
        )

        latent_demand_score = float(
            np.clip(
                opportunity_index * 0.44
                + engagement_rate * 0.18
                + trend_momentum * 0.18
                + (1 - price_sensitivity) * 0.08
                + rng.normal(0, 0.05),
                0,
                1,
            )
        )

        if latent_demand_score >= 0.56:
            demand_classification = "High Demand"
        elif latent_demand_score >= 0.36:
            demand_classification = "Moderate Demand"
        else:
            demand_classification = "Low Demand"

        unmet_demand_flag = int(unmet_need_signal >= 0.62 and demand_classification != "High Demand")
        emerging_trend_flag = int(trend_momentum >= 0.58 and trend_growth > 0.15)
        opportunity_score = round(float(np.clip((opportunity_index * 0.7 + latent_demand_score * 0.3) * 100, 0, 100)), 2)

        rows.append(
            {
                "county": county,
                "topic": topic,
                "time_period": time_period,
                "engagement_intensity": round(float(engagement_intensity), 4),
                "mentions_count": mentions_count,
                "comments_count": comments_count,
                "shares_count": shares_count,
                "likes_count": likes_count,
                "searches_count": searches_count,
                "sentiment_score": round(sentiment_score, 4),
                "urgency_score": round(urgency_score, 4),
                "trend_growth": round(trend_growth, 4),
                "repetition_score": round(repetition_score, 4),
                "location_relevance": round(location_relevance, 4),
                "price_sensitivity": round(price_sensitivity, 4),
                "noise_score": round(noise_score, 4),
                "engagement_rate": round(engagement_rate, 4),
                "weighted_engagement_score": round(weighted_engagement_score, 4),
                "trend_momentum": round(trend_momentum, 4),
                "unmet_need_signal": round(unmet_need_signal, 4),
                "opportunity_index": round(opportunity_index, 4),
                "demand_classification": demand_classification,
                "opportunity_score": opportunity_score,
                "unmet_demand_flag": unmet_demand_flag,
                "emerging_trend_flag": emerging_trend_flag,
            }
        )

    frame = pd.DataFrame(rows)
    _validate_training_frame(frame)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    return frame


def load_training_data(path: str | Path = TRAINING_DATA_PATH) -> pd.DataFrame:
    data_path = Path(path)
    if not data_path.exists():
        return generate_training_data(data_path)
    frame = pd.read_csv(data_path)
    _validate_training_frame(frame)
    return frame


def train_signal_model(
    data_path: str | Path = TRAINING_DATA_PATH,
    model_path: str | Path = MODEL_PATH,
    metadata_path: str | Path = METADATA_PATH,
    random_state: int = 42,
) -> TrainingResult:
    """Train the primary demand-classification pipeline and companion classifiers."""

    frame = load_training_data(data_path)
    if not _has_sufficient_class_balance(frame["demand_classification"]):
        frame = generate_training_data(data_path, random_state=random_state)
    x = frame[PRIMARY_FEATURE_COLUMNS]
    y = frame["demand_classification"]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=random_state,
        stratify=y,
    )

    primary_pipeline = _build_classifier_pipeline(random_state)
    primary_pipeline.fit(x_train, y_train)
    accuracy = accuracy_score(y_test, primary_pipeline.predict(x_test))
    try:
        cv_score = float(cross_val_score(primary_pipeline, x, y, cv=5, scoring="accuracy").mean())
    except Exception:
        cv_score = None

    unmet_pipeline = _build_classifier_pipeline(random_state + 1)
    unmet_pipeline.fit(x, frame["unmet_demand_flag"])

    emerging_pipeline = _build_classifier_pipeline(random_state + 2)
    emerging_pipeline.fit(x, frame["emerging_trend_flag"])

    artifact = {
        "model": primary_pipeline,
        "unmet_model": unmet_pipeline,
        "emerging_model": emerging_pipeline,
        "feature_columns": PRIMARY_FEATURE_COLUMNS,
        "class_labels": DEMAND_CLASS_ORDER,
        "trained_at": datetime.now(UTC).isoformat(),
    }

    model_file = Path(model_path)
    model_file.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_file)

    metadata = {
        "training_date": artifact["trained_at"],
        "features_used": PRIMARY_FEATURE_COLUMNS,
        "model_type": "RandomForestClassifier pipeline",
        "accuracy_score": round(float(accuracy), 4),
        "cross_validation_score": None if cv_score is None else round(cv_score, 4),
        "package_versions": {
            "numpy": version("numpy"),
            "pandas": version("pandas"),
            "scikit-learn": version("scikit-learn"),
            "joblib": version("joblib"),
        },
        "training_rows": len(frame),
        "artifact_path": str(model_file),
        "data_path": str(Path(data_path)),
    }

    metadata_file = Path(metadata_path)
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return TrainingResult(
        model_path=str(model_file),
        metadata_path=str(metadata_file),
        training_rows=len(frame),
        accuracy_score=round(float(accuracy), 4),
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
                PRIMARY_FEATURE_COLUMNS,
            )
        ]
    )
    model = RandomForestClassifier(
        n_estimators=220,
        min_samples_leaf=2,
        random_state=random_state,
        class_weight="balanced_subsample",
    )
    return Pipeline(steps=[("preprocess", preprocessing), ("model", model)])


def _validate_training_frame(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Training data is missing required columns: {', '.join(missing)}")


def _has_sufficient_class_balance(target: pd.Series) -> bool:
    counts = target.value_counts()
    return counts.size >= 3 and int(counts.min()) >= 2


def main() -> None:
    result = train_signal_model()
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
