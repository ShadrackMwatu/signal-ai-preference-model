---
title: Signal AI Dashboard
emoji: 🤗
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.0.0"
app_file: app.py
pinned: false
---

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
It trains from a deterministic 1000+ row synthetic behavioral dataset and
predicts `High`, `Moderate`, or `Low` demand from:

- `likes`
- `comments`
- `shares`
- `searches`

Regenerate the deployed model artifact:

```powershell
.\.venv\Scripts\python.exe -m src.models.signal_demand_model
```

The Gradio app returns the predicted demand classification, aggregate demand
score, and opportunity score. The scores are scaled from the model's highest
class probability.

## Signal CGE Modelling Framework

Signal now has a second, complementary module for policy modelling:

1. Behavioral Signals AI for revealed demand and market intelligence.
2. Signal CGE Modelling Framework for AI-assisted CGE scenario language,
   local execution, GAMS-compatible exports, and policy intelligence.

The CGE framework is additive and does not replace the behavioral-signal model.
The core principle is that GAMS is a modelling language and execution
environment, while solvers are mathematical engines. Signal is developing its
own modelling language and execution environment first, while initially relying
on GAMS and Python solver backends for computation.
It includes:

- Long-format SAM loading, validation, privacy checks, and calibration.
- A compact scenario language such as `shock demand agriculture by 6%`.
- A transparent local comparative-static simulation runner.
- Policy intelligence summaries for GDP, welfare, prices, fiscal balance,
  external balance, sector impacts, risks, and recommended actions.
- GAMS-compatible model text export with sets, SAM parameters, shock scalars,
  equations, model declaration, and solve block.

Sample CGE data lives in:

- `data/sample_sam.csv`
- `data/sample_cge_scenarios.csv`

Run a default scenario locally:

```powershell
.\.venv\Scripts\python.exe -c "from src.cge.framework import run_policy_scenario; print(run_policy_scenario()['macro_results'])"
```

The production-shaped CGE stack is organized as:

- `signal_modeling_language/` for SML grammar, parser, schema, validation, and examples.
- `signal_execution/` for local workflow execution, logs, diagnostics, and outputs.
- `backends/gams/` for GAMS-compatible `.gms`, `.lst`, and GDX helpers.
- `solvers/` for GAMS, experimental Python NLP, and fixed-point backends.
- `cge_core/` for SAM, calibration, accounts, closures, shocks, equations, and results.
- `policy_intelligence/` for reports, scenario comparison, and Kenya policy templates.
- `learning_memory/` for local run-memory records and template/rule recommendations.
- `signal_learning/` for structured learning from SAM structures, model files,
  GAMS logs, solver outcomes, validation errors, user corrections, and final reports.

Run the SML example:

```powershell
.\.venv\Scripts\python.exe -c "from signal_execution.runner import SignalRunner; print(SignalRunner().run('signal_modeling_language/examples/basic_cge.sml')['summary'])"
```

More documentation is available in `docs/`.

Learning memory captures the loop:

```text
model runs -> errors/results/logs -> learning memory -> improved templates/rules -> better future runs
```

It stores aggregate run diagnostics locally as JSONL and proposes template or
validation-rule improvements without silently rewriting source files.

The richer `signal_learning/` layer stores evidence-linked lessons in JSON,
generates `outputs/learning_report.md` after model runs, and supports three
learning modes:

- `observe_only`: record lessons only.
- `recommend`: record lessons and recommend improvements. This is the default.
- `safe_apply`: apply low-risk fixes as versioned adapted templates only.

Every learned rule is linked to a source run, observed error/result, correction
made, and validation status. High-risk fixes are flagged for user review.

The explicit learning workflow is:

```text
Observe -> Diagnose -> Store -> Recommend -> Validate -> Implement -> Re-test -> Remember
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
