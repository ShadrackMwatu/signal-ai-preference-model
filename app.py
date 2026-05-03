"""Hugging Face app entrypoint for Signal ML-based demand prediction."""

from __future__ import annotations

from src.models.signal_demand_model import load_signal_model, predict_signal_demand


MODEL_BUNDLE = load_signal_model()


def signal_model(
    likes: int,
    comments: int,
    shares: int,
    searches: int,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    """Predict demand class and learned probability scores using the trained model."""

    prediction = predict_signal_demand(
        {
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "searches": searches,
            "engagement_intensity": engagement_intensity,
            "purchase_intent_score": purchase_intent_score,
            "trend_growth": trend_growth,
        }
    )
    return (
        str(prediction["demand_class"]),
        float(prediction["confidence_score"]),
        float(prediction["opportunity_score"]),
    )


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
            gr.Number(label="Confidence Score"),
            gr.Number(label="Opportunity Score"),
        ],
        title="Signal Demand Prediction",
    )
else:
    demo = None


if __name__ == "__main__" and demo is not None:
    demo.launch()
