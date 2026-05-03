"""FastAPI API for modular Signal market intelligence."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

from src.data_pipeline.data_loader import load_behavioral_signals
from src.data_pipeline.synthetic_data import SAMPLE_BEHAVIORAL_PATH, SAMPLE_COMPETITOR_PATH, write_sample_data
from src.features.aggregation import aggregate_features
from src.features.feature_engineering import build_feature_table
from src.models.clustering_model import SegmentClusterer
from src.models.predict_demand import DemandPredictor
from src.models.train_demand_model import DemandModelBundle, train_demand_models


app = FastAPI(title="Signal Market Intelligence", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/predict-demand")
def predict_demand() -> list[dict[str, object]]:
    predictor = DemandPredictor(_model_bundle())
    predictions = predictor.predict(_signals(), _competitors())
    return _safe_records(predictions)


@app.get("/county-demand")
def county_demand() -> dict[str, object]:
    predictions = pd.DataFrame(predict_demand())
    county = (
        predictions.groupby("county", as_index=False)["aggregate_demand_score"].mean().round(4)
        .rename(columns={"aggregate_demand_score": "county_demand_index"})
        .to_dict(orient="records")
    )
    national = round(float(predictions["aggregate_demand_score"].mean()), 4)
    category = (
        predictions.groupby("category", as_index=False)["aggregate_demand_score"].mean().round(4)
        .rename(columns={"aggregate_demand_score": "category_preference_index"})
        .to_dict(orient="records")
    )
    return {
        "national_aggregate_demand_index": national,
        "county_demand_index": county,
        "category_preference_index": category,
    }


@app.get("/opportunities")
def opportunities() -> list[dict[str, object]]:
    predictions = pd.DataFrame(predict_demand())
    fields = [
        "country",
        "county",
        "category",
        "consumer_segment",
        "time_period",
        "opportunity_score",
        "demand_classification",
        "recommended_value_proposition",
        "product_or_service_opportunity",
        "revenue_model",
        "competitor_gap",
        "supplier_recommendation",
        "logistics_recommendation",
        "payment_recommendation",
    ]
    return predictions.sort_values("opportunity_score", ascending=False).head(20)[fields].to_dict(orient="records")


@app.get("/segments")
def segments() -> list[dict[str, object]]:
    features = build_feature_table(_signals())
    clusterer = SegmentClusterer().fit(features)
    return clusterer.predict(features).to_dict(orient="records")


@app.get("/market-access")
def market_access() -> list[dict[str, object]]:
    predictions = pd.DataFrame(predict_demand())
    fields = [
        "country",
        "county",
        "category",
        "consumer_segment",
        "pricing_power",
        "customer_reach",
        "inventory_planning",
        "sales_forecasting",
        "market_entry_strategy",
        "supplier_recommendation",
        "logistics_recommendation",
        "payment_recommendation",
    ]
    return predictions[fields].to_dict(orient="records")


def create_app() -> FastAPI:
    return app


@lru_cache(maxsize=1)
def _model_bundle() -> DemandModelBundle:
    signals = _signals()
    features = aggregate_features(build_feature_table(signals))
    return train_demand_models(features)


@lru_cache(maxsize=1)
def _signals() -> pd.DataFrame:
    if not Path(SAMPLE_BEHAVIORAL_PATH).exists():
        write_sample_data()
    return load_behavioral_signals(SAMPLE_BEHAVIORAL_PATH)


@lru_cache(maxsize=1)
def _competitors() -> pd.DataFrame:
    if not Path(SAMPLE_COMPETITOR_PATH).exists():
        write_sample_data()
    return pd.read_csv(SAMPLE_COMPETITOR_PATH)


def _safe_records(frame: pd.DataFrame) -> list[dict[str, object]]:
    blocked = {"signal_id", "text"}
    return frame[[column for column in frame.columns if column not in blocked]].to_dict(orient="records")
