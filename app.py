"""Hugging Face app entrypoint for Signal ML-based demand prediction."""

from __future__ import annotations

from pathlib import Path

from joblib import load

from src.models.signal_demand_model import FEATURE_COLUMNS, MODEL_PATH, train_signal_model


def _load_deployed_model():
    model_path = Path(MODEL_PATH)
    if not model_path.exists():
        train_signal_model(model_path=model_path)
    loaded_model = load(model_path)
    if isinstance(loaded_model, dict) and "model" in loaded_model:
        loaded_model = loaded_model["model"]
    if getattr(loaded_model, "n_features_in_", len(FEATURE_COLUMNS)) != len(FEATURE_COLUMNS):
        train_signal_model(model_path=model_path)
        loaded_model = load(model_path)
    return loaded_model


model = _load_deployed_model()


def signal_model(
    likes: int,
    comments: int,
    shares: int,
    searches: int,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    """Predict demand class from the trained four-signal ML model."""

    features = [[likes, comments, shares, searches]]
    prediction = str(model.predict(features)[0])
    confidence = float(model.predict_proba(features).max())
    aggregate_demand_score = round(confidence * 100, 2)
    opportunity_score = round(confidence * 100, 2)
    return prediction, aggregate_demand_score, opportunity_score


try:
    import gradio as gr
except ImportError:
    gr = None


if gr is not None:
    demo = gr.Interface(
        fn=signal_model,
        inputs=[
            gr.Number(label="Likes", value=120, precision=0),
            gr.Number(label="Comments", value=35, precision=0),
            gr.Number(label="Shares", value=24, precision=0),
            gr.Number(label="Searches", value=160, precision=0),
            gr.Slider(0, 1, value=0.55, label="Engagement Intensity"),
            gr.Slider(0, 1, value=0.7, label="Purchase Intent Score"),
            gr.Slider(0, 1, value=0.35, label="Trend Growth"),
        ],
        outputs=[
            gr.Textbox(label="Predicted Demand Class"),
            gr.Number(label="Aggregate Demand Score"),
            gr.Number(label="Opportunity Score"),
        ],
        title="Signal Demand Prediction",
    )
else:
    demo = None


if __name__ == "__main__" and demo is not None:
    demo.launch()
