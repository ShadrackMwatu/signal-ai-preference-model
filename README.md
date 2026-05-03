# Signal AI Preference Model

Signal is a small Python prototype for learning user-item preferences and serving
preference scores through a FastAPI API.

## What is included

- CSV loading and validation for labeled preference examples.
- A scikit-learn logistic regression pipeline with categorical and numeric features.
- Model evaluation, persistence, and reload support.
- FastAPI endpoints for health checks, prediction, batch prediction, and retraining.
- Sample preference data and tests.

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
