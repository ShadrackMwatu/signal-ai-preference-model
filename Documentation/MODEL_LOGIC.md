# Model Logic

Last updated: 2026-05-08

## Model Families

Signal contains several modeling layers:

- Dashboard demand model in `app.py`.
- Training pipeline in `train_model.py`.
- Demand model utilities in `src/models/`.
- ML utilities in `ml/`.
- Preference model in `src/model.py`.

## Training Pipeline

`train_model.py` supports:

- synthetic training data generation
- loading training data
- preparing feature frames
- classifier pipeline construction
- safe train/test split
- cross-validation
- versioned artifact writing

## Prediction Fields

Common prediction outputs include:

- `demand_classification`
- `confidence_score`
- `aggregate_demand_score`
- `opportunity_score`
- `emerging_trend_probability`
- `unmet_demand_probability`
- `investment_opportunity_interpretation`
- `model_source_label`

## Fallback Logic

Fallback logic exists to keep the platform operational when model artifacts are unavailable. It is not a replacement for trained models; it is a resilience mechanism.

## Model Registry

`ml/model_registry.py` stores records for trained models and supports version tracking.

## Evaluation

Evaluation helpers live in:

- `src/evaluation/metrics.py`
- `ml/model_evaluation.py`

