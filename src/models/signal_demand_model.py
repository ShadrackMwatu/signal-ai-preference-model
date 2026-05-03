"""ML-based demand classifier for the deployed Signal app."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


ROOT_DIR = Path(__file__).resolve().parents[2]
TRAINING_DATA_PATH = ROOT_DIR / "data" / "signal_training_dataset.csv"
MODEL_PATH = ROOT_DIR / "model.pkl"
FEATURE_COLUMNS = [
    "likes",
    "comments",
    "shares",
    "searches",
    "engagement_intensity",
    "purchase_intent_score",
    "trend_growth",
]
TARGET_COLUMN = "demand_class"
DEMAND_CLASSES = ("High", "Moderate", "Low")


def generate_training_dataset(
    path: str | Path = TRAINING_DATA_PATH,
    n_rows: int = 1200,
    random_state: int = 42,
) -> pd.DataFrame:
    """Generate synthetic behavioral training data for the deployed demand classifier."""

    rng = np.random.default_rng(random_state)
    rows: list[dict[str, float | int | str]] = []
    for _ in range(n_rows):
        latent_interest = rng.beta(2.2, 2.0)
        engagement_intensity = float(np.clip(rng.normal(latent_interest, 0.16), 0, 1))
        purchase_intent_score = float(np.clip(rng.normal(latent_interest, 0.18), 0, 1))
        trend_growth = float(np.clip(rng.normal(latent_interest, 0.2), 0, 1))
        likes = int(rng.poisson(20 + engagement_intensity * 230))
        comments = int(rng.poisson(4 + engagement_intensity * 45 + purchase_intent_score * 35))
        shares = int(rng.poisson(2 + engagement_intensity * 34 + trend_growth * 36))
        searches = int(rng.poisson(12 + purchase_intent_score * 260 + trend_growth * 80))
        latent_score = (
            0.3 * engagement_intensity
            + 0.38 * purchase_intent_score
            + 0.22 * trend_growth
            + 0.08 * min(1.0, searches / 220)
            + float(rng.normal(0, 0.035))
        )
        demand_class = _class_from_score(latent_score)
        rows.append(
            {
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "searches": searches,
                "engagement_intensity": round(engagement_intensity, 4),
                "purchase_intent_score": round(purchase_intent_score, 4),
                "trend_growth": round(trend_growth, 4),
                "demand_class": demand_class,
            }
        )

    frame = pd.DataFrame(rows)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def train_signal_model(
    data_path: str | Path = TRAINING_DATA_PATH,
    model_path: str | Path = MODEL_PATH,
    random_state: int = 42,
) -> dict[str, float | int | str]:
    """Train and save the deployed Signal demand classifier."""

    data_path = Path(data_path)
    if not data_path.exists():
        generate_training_dataset(data_path, random_state=random_state)
    frame = pd.read_csv(data_path)
    model = RandomForestClassifier(n_estimators=120, min_samples_leaf=3, random_state=random_state)
    x_train, x_test, y_train, y_test = train_test_split(
        frame[FEATURE_COLUMNS],
        frame[TARGET_COLUMN],
        test_size=0.25,
        random_state=random_state,
        stratify=frame[TARGET_COLUMN],
    )
    model.fit(x_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(x_test))
    save_path = Path(model_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_columns": FEATURE_COLUMNS}, save_path)
    return {
        "model_path": str(save_path),
        "training_rows": len(frame),
        "accuracy": round(float(accuracy), 4),
    }


def load_signal_model(model_path: str | Path = MODEL_PATH) -> dict[str, object]:
    """Load the saved classifier, training it first if needed."""

    model_path = Path(model_path)
    if not model_path.exists():
        train_signal_model(model_path=model_path)
    return joblib.load(model_path)


def predict_signal_demand(features: dict[str, float | int], model_path: str | Path = MODEL_PATH) -> dict[str, float | str]:
    """Predict demand class, confidence, and opportunity from behavioral features."""

    bundle = load_signal_model(model_path)
    model = bundle["model"]
    feature_columns = bundle["feature_columns"]
    missing = [column for column in feature_columns if column not in features]
    if missing:
        raise ValueError(f"Missing required feature(s): {', '.join(missing)}")
    frame = pd.DataFrame([{column: features[column] for column in feature_columns}])
    predicted_class = str(model.predict(frame)[0])
    probabilities = {
        str(class_name): float(probability)
        for class_name, probability in zip(model.classes_, model.predict_proba(frame)[0], strict=True)
    }
    confidence_score = probabilities[predicted_class]
    opportunity_score = probabilities.get("High", 0.0)
    return {
        "demand_class": predicted_class,
        "confidence_score": round(confidence_score, 4),
        "opportunity_score": round(opportunity_score, 4),
        "score": round(confidence_score, 4),
    }


def _class_from_score(score: float) -> str:
    if score >= 0.66:
        return "High"
    if score >= 0.42:
        return "Moderate"
    return "Low"


if __name__ == "__main__":
    print(train_signal_model())
