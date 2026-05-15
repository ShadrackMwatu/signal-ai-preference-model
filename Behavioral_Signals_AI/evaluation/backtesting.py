"""Backtesting helpers for lightweight prediction memory."""

from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.adaptive_learning.prediction_memory import load_prediction_memory
from Behavioral_Signals_AI.evaluation.model_metrics import compute_model_metrics


def backtest_prediction_memory(path: str | Path | None = None, limit: int = 500) -> dict:
    records = load_prediction_memory(limit=limit, path=path)
    return compute_model_metrics(records)