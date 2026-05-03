"""FastAPI application for serving Signal preference predictions."""

from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.data import load_examples
from src.model import PreferenceModel
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


app = create_app()
