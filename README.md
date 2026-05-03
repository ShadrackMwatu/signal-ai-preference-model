# Signal AI Preference Model

Signal is a small Python prototype for learning user-item preferences and serving
preference scores through a FastAPI API.

## What is included

- CSV loading and validation for labeled preference examples.
- A scikit-learn logistic regression pipeline with categorical and numeric features.
- Model evaluation, persistence, and reload support.
- FastAPI endpoints for health checks, prediction, batch prediction, and retraining.
- Interpretable drivers, policy signal labels, and CGE/SAM-ready export rows.
- Sample preference data and tests.

## Research outputs

Every model prediction includes:

- `drivers`: coefficient-weighted feature contributions for interpretation.
- `policy_signal`: a policy-facing label for the preference strength and direction.
- `cge_sam_account`: a stable account mapping for CGE/SAM workflows.
- `cge_sam_shock`: a centered shock value that can feed scenario analysis.
- `publication_notes`: method and validation notes for academic reporting.

The `src.research.export_cge_sam_csv` helper writes export-ready CSV files for
integration with CGE/SAM pipelines.

## Module 1: Data Ingestion

Module 1 generates and validates deterministic synthetic preference data:

```powershell
.\.venv\Scripts\python.exe -m src.data_ingestion --output data\synthetic_preferences.csv
```

The generated dataset covers policy, operations, research, and planning user
segments across analytics, automation, forecasting, and research categories.

## Adaptive Demand Intelligence

Signal now includes a privacy-preserving market intelligence pipeline:

```text
behavioral data -> feature extraction -> model training -> prediction
-> recommendation -> feedback -> retraining
```

It uses anonymized country/county/category/consumer-segment/time-period
behavioral signals only. The learned models predict demand class, aggregate
demand, opportunity, trend and unmet-demand probabilities, likely market gaps,
value propositions, product/service opportunities, revenue models, market-entry
strategy, competitor gaps, price gaps, service gaps, delivery gaps, and
supplier/logistics/payment recommendations. Adaptive retraining records drift
scores, retraining decisions, records used, and model versions.

Privacy safeguards reject PII, usernames, phone numbers, emails, exact GPS
fields, psychological targeting fields, and small-cell segment reporting.

Generate the modular Kenya behavioral, competitor, and feedback samples:

```powershell
.\.venv\Scripts\python.exe -m src.data_pipeline.synthetic_data --data-dir data
```

Modular API endpoints:

- `GET /health`
- `GET /predict-demand`
- `GET /county-demand`
- `GET /opportunities`
- `GET /segments`
- `GET /market-access`

## Deployed ML Demand Model

The deployed app entrypoint, `app.py`, loads a saved scikit-learn
`RandomForestClassifier` from `models/saved_models/signal_demand_classifier.joblib`.
It predicts `High`, `Moderate`, or `Low` demand from:

- `likes`
- `comments`
- `shares`
- `searches`
- `engagement_intensity`
- `purchase_intent_score`
- `trend_growth`

Regenerate the deployed model artifact:

```powershell
.\.venv\Scripts\python.exe -m src.models.signal_demand_model
```

## Run locally

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```
