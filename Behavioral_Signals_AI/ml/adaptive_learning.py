"""Adaptive learning loop for Signal ML predictions and observed outcomes."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from .model_training import train_demand_classifier


DOMAIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORY_PATH = DOMAIN_ROOT / "models_ml" / "metadata" / "prediction_history.jsonl"


class AdaptiveLearningStore:
    """Append-only local store for predictions and observed outcomes."""

    def __init__(self, path: str | Path = DEFAULT_HISTORY_PATH) -> None:
        self.path = Path(path)

    def record_prediction(self, prediction: dict[str, Any]) -> str:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "record_type": "prediction",
            **prediction,
        }
        return self._append(entry)

    def record_outcome(self, outcome: dict[str, Any]) -> str:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "record_type": "observed_outcome",
            **outcome,
        }
        return self._append(entry)

    def read_history(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def _append(self, entry: dict[str, Any]) -> str:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")
        return str(self.path)


def compare_predictions_with_outcomes(
    predictions: pd.DataFrame,
    outcomes: pd.DataFrame,
    key_columns: list[str],
    predicted_column: str = "prediction",
    observed_column: str = "observed_outcome",
) -> pd.DataFrame:
    """Join predictions to later observed outcomes for adaptive evaluation."""

    merged = predictions.merge(outcomes, on=key_columns, how="inner", suffixes=("_predicted", "_observed"))
    merged["prediction_matched_outcome"] = merged[predicted_column] == merged[observed_column]
    return merged


def retrain_when_labelled_data_available(
    labelled_data: pd.DataFrame,
    target_column: str = "demand_class",
    minimum_rows: int = 30,
    model_name: str = "adaptive_signal_demand_classifier",
    output_dir: str | Path = DOMAIN_ROOT / "models_ml" / "trained_models",
    registry: Any | None = None,
) -> dict[str, Any]:
    """Retrain the default classifier when enough labelled data is available."""

    if len(labelled_data) < minimum_rows or target_column not in labelled_data.columns:
        return {
            "retrained": False,
            "prediction_source": "adaptive learning update",
            "message": "Not enough labelled data available for retraining.",
            "records_available": len(labelled_data),
        }
    result = train_demand_classifier(
        labelled_data,
        target_column=target_column,
        model_name=model_name,
        output_dir=output_dir,
        registry=registry,
    )
    return {
        "retrained": True,
        "prediction_source": "adaptive learning update",
        "model_path": result["model_path"],
        "metrics": result["metrics"],
        "model_version": result["registry_record"].version,
        "records_available": len(labelled_data),
    }
