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
