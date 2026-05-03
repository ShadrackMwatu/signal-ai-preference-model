"""Classification, regression, drift, and retraining metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, precision_score, recall_score


def model_metrics(y_true_class, y_pred_class, y_true_score, y_pred_score) -> dict[str, float]:
    """Compute the required classification and regression metrics."""

    return {
        "accuracy": round(float(accuracy_score(y_true_class, y_pred_class)), 4),
        "precision": round(float(precision_score(y_true_class, y_pred_class, average="weighted", zero_division=0)), 4),
        "recall": round(float(recall_score(y_true_class, y_pred_class, average="weighted", zero_division=0)), 4),
        "f1": round(float(f1_score(y_true_class, y_pred_class, average="weighted", zero_division=0)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true_score, y_pred_score))), 4),
        "mae": round(float(mean_absolute_error(y_true_score, y_pred_score)), 4),
    }


def evaluate_predictions(feature_frame: pd.DataFrame, predictions: pd.DataFrame) -> dict[str, float]:
    """Evaluate model outputs where supervised labels are available."""

    return model_metrics(
        feature_frame["demand_classification"],
        predictions["demand_classification"],
        feature_frame["aggregate_demand_score"],
        predictions["aggregate_demand_score"],
    )
