from __future__ import annotations

from pathlib import Path

from Behavioral_Signals_AI.adaptive_learning.accuracy_tracker import evaluate_prediction_accuracy, summarize_accuracy
from Behavioral_Signals_AI.adaptive_learning.online_calibrator import calibrate_prediction
from Behavioral_Signals_AI.adaptive_learning.prediction_memory import load_prediction_memory, save_prediction_snapshot
from Behavioral_Signals_AI.backend import run_behavioral_intelligence_pipeline
from Behavioral_Signals_AI.evaluation.backtesting import backtest_prediction_memory


def test_prediction_memory_write_and_read(tmp_path: Path):
    memory_file = tmp_path / "prediction_memory.jsonl"
    saved = save_prediction_snapshot(
        {
            "signal_name": "maize flour prices",
            "category": "food_agriculture",
            "source": "Google Trends",
            "predicted_demand_level": "High",
            "predicted_opportunity": 82,
            "confidence": 78,
            "username": "must_not_store",
        },
        path=memory_file,
    )
    rows = load_prediction_memory(path=memory_file)

    assert saved["privacy_level"] == "aggregate_public"
    assert "username" not in saved
    assert rows[0]["signal_name"] == "maize flour prices"


def test_adaptive_weight_updates_cross_source_confirmation():
    history = [
        {"signal_name": "fuel prices", "source": "Google Trends", "category": "prices", "accuracy_score": 82},
        {"signal_name": "fuel prices", "source": "X", "category": "prices", "accuracy_score": 76},
    ]
    calibrated = calibrate_prediction({"signal_name": "fuel prices", "source": "GDELT", "category": "prices", "growth": "rising", "search_intensity": 120000}, history)

    assert calibrated["cross_provider_confirmation"] == 3
    assert calibrated["adaptive_confidence"] > 50
    assert calibrated["learning_status"] == "adaptive_rule_based"


def test_accuracy_tracking_and_backtesting(tmp_path: Path):
    memory_file = tmp_path / "prediction_memory.jsonl"
    save_prediction_snapshot({"signal_name": "jobs", "predicted_demand_level": 70, "actual_follow_up_signal_strength": 66, "category": "jobs"}, path=memory_file)
    rows = load_prediction_memory(path=memory_file)
    result = evaluate_prediction_accuracy(rows[0])
    summary = summarize_accuracy(rows)
    backtest = backtest_prediction_memory(path=memory_file)

    assert result["accuracy_result"] == "accurate"
    assert summary["evaluated_predictions"] == 1
    assert backtest["prediction_count"] == 1


def test_adaptive_pipeline_adds_forecasts_and_memory(monkeypatch, tmp_path: Path):
    memory_file = tmp_path / "prediction_memory.jsonl"
    monkeypatch.setenv("SIGNAL_PREDICTION_MEMORY_PATH", str(memory_file))
    result = run_behavioral_intelligence_pipeline(
        [
            {
                "signal_name": "hospital near me",
                "source": "Google Trends",
                "provider_type": "search",
                "category": "health",
                "location": "Kenya",
                "search_intensity": 90000,
                "growth": "rising",
                "confidence": 0.8,
            }
        ]
    )

    signal = result["signals"][0]
    assert signal["predicted_demand_level"] in {"High", "Moderate", "Emerging", "Low"}
    assert "predicted_opportunity_score" in signal
    assert "adaptive_confidence" in signal
    assert load_prediction_memory(path=memory_file)