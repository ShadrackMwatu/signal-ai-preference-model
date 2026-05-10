# Signal Development Log

Last updated: 2026-05-08

## Summary

Signal has evolved from a preference prediction project into a multi-layer AI, public intelligence, and economic modeling platform. This log records major implementation decisions, debugging events, and architectural additions.

## Major Enhancements

### Behavioral Signals AI

- Built a Gradio dashboard around aggregate behavioral inputs: likes, comments, shares, searches, engagement intensity, purchase intent score, and trend growth.
- Added demand classification, confidence score, aggregate demand score, opportunity score, emerging trend probability, and unmet demand probability.
- Added fallback prediction logic so the app remains usable when model artifacts are missing.
- Added guardrails to avoid over-interpreting weak, noisy, or low-confidence signals.
- Added explanation outputs, risk signals, and "why this matters" notes.

### UI Upgrades

- Added visual cards for confidence, signal strength, trend momentum, opportunity radar, and key drivers.
- Added immediate visible `Live Trend Intelligence` HTML card near the top of Behavioral Signals AI.
- Experimented with hidden tables and animated trend feeds, then applied an emergency minimal patch to guarantee first-paint visibility.
- Disabled public Gradio API schema exposure for dashboard callbacks to reduce schema-related runtime fragility.

### Live Trends Embedding

- Implemented `x_trends.py` for public aggregate X/Twitter trend retrieval.
- Added fallback demo trends when `X_BEARER_TOKEN` is missing or the API is unavailable.
- Implemented `trend_intelligence.py` for trend proxy features and batch summaries.
- Embedded trend intelligence inside Behavioral Signals AI instead of a separate top-level tab.
- Added an emergency circular-import fix by removing imports from `trend_intelligence.py` to `app.py`.

### Adaptive Learning Integration

- Added feedback logging in `adaptive_learning.py`.
- Added `learning_memory/` for run memories, patterns, schemas, and recommendations.
- Added `signal_learning/` for observe, diagnose, store, recommend, validate, implement, retest, and remember workflows.
- Added Gradio Learning tab controls for lessons, recurring issues, recommended fixes, safe apply, ignore, and rollback.

### SML/CGE Workbench

- Added SML parsing, validation, examples, and workbench helpers.
- Added SAM loading, balance checks, calibration, and GAMS-compatible export support.
- Added solver abstraction and execution runner.
- Added policy intelligence reporting and scenario comparison.
- Added Gradio SML CGE Workbench tab for validation and run workflows.

### GitHub And Hugging Face

- Added GitHub Actions workflow to sync the repository to a Hugging Face Space.
- Kept `app.py`, `requirements.txt`, and README Space metadata at repo root.
- Added deployment notes for Hugging Face tokens and fallback behavior.

## Runtime Errors And Resolutions

### Circular Import And Button `_id`

Cause: `trend_intelligence.py` imported `predict_demand_details` from `app.py`, causing `app.py` to be imported while Gradio components were still being constructed.

Resolution: remove imports from `app.py` inside `trend_intelligence.py` and add a local lightweight fallback predictor.

### Callback Output Mismatch

Cause: experimental callback revisions returned values in an order that did not match Gradio outputs or included extra outputs.

Resolution: keep callback returns aligned with output lists and avoid returning component objects.

### Hidden DataFrame Vs Visible Feed

Cause: trend intelligence was represented both as tables and as HTML. Public UI requirements shifted toward visible animated feed only.

Resolution: hide DataFrames with `visible=False` and expose only HTML feed where required.

### Hugging Face Startup Issues

Cause: missing optional credentials, model artifacts, version compatibility, and runtime import constraints.

Resolution: use demo fallback trends, fallback prediction logic, root-level Space metadata, and constrained dependency versions.

## Current State

The app currently supports Behavioral Signals AI, visible Live Trend Intelligence, Signal CGE Framework, SML CGE Workbench, and Learning tabs. The docs system now records architecture, deployment, debugging, privacy, roadmap, and implementation history.

