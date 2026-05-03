"""FastAPI application for serving Signal preference predictions."""

from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.data import load_examples
from src.data_pipeline import DEFAULT_BEHAVIORAL_DATA_PATH, load_behavioral_data, write_behavioral_dataset
from src.evaluation import evaluate_signal_system
from src.model import PreferenceModel
from src.models import SignalDemandIntelligenceSystem
from src.research import cge_sam_row
from src.schemas import PreferenceRequest


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = ROOT_DIR / "data" / "sample_preferences.csv"
DEFAULT_MODEL_PATH = ROOT_DIR / "models" / "signal_model.joblib"


class PreferencePayload(BaseModel):
    user_id: str = Field(min_length=1)
    item_id: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(ge=0)
    rating: float = Field(ge=0, le=5)
    popularity: float = Field(ge=0, le=1)


class FeatureContributionResponse(BaseModel):
    feature: str
    value: str
    contribution: float
    direction: str


class PredictionResponse(BaseModel):
    item_id: str
    score: float
    preferred: bool
    drivers: list[FeatureContributionResponse]
    policy_signal: str
    cge_sam_account: str
    cge_sam_shock: float
    publication_notes: list[str]


class BatchPreferencePayload(BaseModel):
    items: list[PreferencePayload] = Field(min_length=1)


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class CgeSamExportPayload(BaseModel):
    scenario_id: str = Field(default="baseline", min_length=1)
    items: list[PreferencePayload] = Field(min_length=1)


class CgeSamRowResponse(BaseModel):
    scenario_id: str
    user_id: str
    item_id: str
    category: str
    sam_account: str
    preference_score: float
    preferred: bool
    shock_value: float
    shock_direction: str
    top_driver: str


class CgeSamExportResponse(BaseModel):
    rows: list[CgeSamRowResponse]


def create_app(model_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Signal AI Preference Model",
        version="0.1.0",
        description="Prototype API for scoring user-item preference likelihood.",
    )

    app.state.model_path = Path(model_path or os.getenv("SIGNAL_MODEL_PATH", DEFAULT_MODEL_PATH))
    app.state.model = _load_or_train_model(app.state.model_path)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PreferencePayload) -> PredictionResponse:
        prediction = app.state.model.predict(_payload_to_request(payload))
        return PredictionResponse(**asdict(prediction))

    @app.post("/predict/batch", response_model=BatchPredictionResponse)
    def predict_batch(payload: BatchPreferencePayload) -> BatchPredictionResponse:
        requests = [_payload_to_request(item) for item in payload.items]
        predictions = app.state.model.predict_many(requests)
        return BatchPredictionResponse(
            predictions=[PredictionResponse(**asdict(prediction)) for prediction in predictions]
        )

    @app.post("/export/cge-sam", response_model=CgeSamExportResponse)
    def export_cge_sam(payload: CgeSamExportPayload) -> CgeSamExportResponse:
        requests = [_payload_to_request(item) for item in payload.items]
        predictions = app.state.model.predict_many(requests)
        rows = [
            CgeSamRowResponse(**cge_sam_row(request, prediction, payload.scenario_id))
            for request, prediction in zip(requests, predictions, strict=True)
        ]
        return CgeSamExportResponse(rows=rows)

    @app.post("/train")
    def train() -> dict[str, float | str]:
        examples = load_examples(DEFAULT_DATA_PATH)
        model = PreferenceModel().train(examples)
        metrics = model.evaluate(examples)
        model.save(app.state.model_path)
        app.state.model = model
        return {"status": "trained", **metrics}

    @app.get("/market-intelligence/dashboard")
    def market_intelligence_dashboard() -> dict[str, object]:
        system = _get_market_system(app)
        frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        return system.predict(frame)

    @app.get("/market-intelligence/evaluation")
    def market_intelligence_evaluation() -> dict[str, dict[str, float]]:
        system = _get_market_system(app)
        frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        return evaluate_signal_system(system, frame)

    @app.post("/market-intelligence/retrain")
    def market_intelligence_retrain() -> dict[str, object]:
        frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        system = _get_market_system(app)
        log = system.retrain_if_needed(frame, force=True)
        app.state.market_system = system
        return {
            "status": "retrained",
            "drift_score": log.drift_score,
            "drifted_features": log.drifted_features,
            "retraining_triggered": log.retraining_triggered,
            "records_used": log.records_used,
        }

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard() -> HTMLResponse:
        system = _get_market_system(app)
        frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        summary = system.predict(frame)["dashboard"]
        html = _dashboard_html(summary)
        return HTMLResponse(content=html)

    return app


def _payload_to_request(payload: PreferencePayload) -> PreferenceRequest:
    return PreferenceRequest(
        user_id=payload.user_id,
        item_id=payload.item_id,
        category=payload.category,
        price=payload.price,
        rating=payload.rating,
        popularity=payload.popularity,
    )


def _load_or_train_model(model_path: Path) -> PreferenceModel:
    if model_path.exists():
        return PreferenceModel.load(model_path)
    if not DEFAULT_DATA_PATH.exists():
        raise HTTPException(status_code=503, detail="No trained model or sample data available")

    examples = load_examples(DEFAULT_DATA_PATH)
    model = PreferenceModel().train(examples)
    model.save(model_path)
    return model


def _get_market_system(app: FastAPI) -> SignalDemandIntelligenceSystem:
    if getattr(app.state, "market_system", None) is None:
        if not DEFAULT_BEHAVIORAL_DATA_PATH.exists():
            write_behavioral_dataset(DEFAULT_BEHAVIORAL_DATA_PATH)
        frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        app.state.market_system = SignalDemandIntelligenceSystem().fit(frame)
    return app.state.market_system


def _dashboard_html(summary: dict[str, object]) -> str:
    opportunities = summary["market_opportunities"][:5]
    opportunity_rows = "".join(
        "<tr>"
        f"<td>{item['county']}</td>"
        f"<td>{item['category']}</td>"
        f"<td>{item['opportunity_score']}</td>"
        f"<td>{item['demand_classification']}</td>"
        f"<td>{item['recommended_value_proposition']}</td>"
        f"<td>{item['supplier_recommendation']}</td>"
        f"<td>{item['logistics_recommendation']}</td>"
        f"<td>{item['payment_recommendation']}</td>"
        "</tr>"
        for item in opportunities
    )
    county_rows = "".join(
        f"<li>{item['county']}: {item['county_demand_index']}</li>"
        for item in summary["county_demand_index"]
    )
    return f"""
    <!doctype html>
    <html>
      <head>
        <title>Signal Market Intelligence Dashboard</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 32px; color: #17202a; }}
          table {{ border-collapse: collapse; width: 100%; }}
          th, td {{ border: 1px solid #d5d8dc; padding: 8px; text-align: left; }}
          th {{ background: #eef2f3; }}
          .metric {{ font-size: 28px; font-weight: 700; }}
        </style>
      </head>
      <body>
        <h1>Signal Market Intelligence Dashboard</h1>
        <p class="metric">National aggregate demand index: {summary['national_aggregate_demand_index']}</p>
        <p>Trend direction: {summary['trend_direction']}</p>
        <h2>County-level Demand</h2>
        <ul>{county_rows}</ul>
        <h2>Market Opportunities</h2>
        <table>
          <thead>
            <tr>
              <th>County</th><th>Category</th><th>Opportunity</th><th>Demand</th>
              <th>Value proposition</th><th>Supplier</th><th>Logistics</th><th>Payment</th>
            </tr>
          </thead>
          <tbody>{opportunity_rows}</tbody>
        </table>
      </body>
    </html>
    """


app = create_app()
