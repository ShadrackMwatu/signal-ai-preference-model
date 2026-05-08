# Debugging And Fixes

Last updated: 2026-05-08

## Circular Import Between `app.py` And `trend_intelligence.py`

### Symptom

Gradio failed with:

```text
AttributeError: 'Button' object has no attribute '_id'
```

### Cause

`trend_intelligence.py` imported `predict_demand_details` from `app.py`. During Gradio UI construction, this could re-import `app.py` before components were fully initialized.

### Fix

- Removed the import from `trend_intelligence.py`.
- Added a local lightweight `predict_demand_details` fallback inside `trend_intelligence.py`.
- Preserved the UI layout and callbacks.

### Lesson

Code imported by `app.py` must not import `app.py` back. Shared prediction logic should eventually move into a neutral service module such as `signal_core/prediction.py`.

## Gradio Button `_id` Issue

### Cause

The `_id` error was a secondary symptom of Gradio component initialization being interrupted by re-imports or component-object misuse.

### Fix

- Break circular imports.
- Return plain values from callbacks.
- Avoid returning `gr.Number`, `gr.HTML`, `gr.Dataframe`, or other component objects from callback functions.

## Callback Mismatch Problems

### Cause

Gradio expects callback return values to match the output component list exactly.

### Fix

Callbacks were adjusted so values align with the declared outputs. Tables receive DataFrames, HTML components receive strings, numbers receive numeric values, and textboxes receive strings.

## Hugging Face Startup Errors

### Causes

- Missing optional API tokens.
- Model artifacts may be missing in some deployment contexts.
- Dependency constraints in hosted runtimes.
- Circular imports during app import.

### Fixes

- Use fallback demo trends when `X_BEARER_TOKEN` is absent.
- Use fallback prediction logic when trained model artifacts are unavailable.
- Keep `requirements.txt` conservative.
- Remove app circular imports.

## `pydub` / `audioop` Issues

### Context

Some hosted Python environments can fail when optional audio dependencies expect modules such as `audioop`.

### Strategy

Signal does not require audio processing for current core behavior. Avoid unnecessary audio dependencies in `requirements.txt`; keep the dashboard focused on Gradio, pandas, numpy, scikit-learn, joblib, openpyxl, FastAPI, and pydantic.

## Missing Model Handling

### Cause

The main trained model may not always exist in a fresh environment.

### Fix

`app.py` uses `_load_prediction_artifact` and `_predict_with_fallback` so the app remains operational without a model file.

## Fallback Prediction Logic

Fallback logic supports:

- Demand band estimation.
- Confidence approximation.
- Opportunity scoring.
- Emerging and unmet demand probabilities.

It should be treated as a resilience layer, not as the long-term primary intelligence engine.

## Matplotlib Cache Warnings

### Symptom

Local test runs can show permission warnings around `.matplotlib` and temporary font cache files.

### Cause

Restricted write access to default cache folders.

### Impact

These warnings did not block app compile or launch checks.

