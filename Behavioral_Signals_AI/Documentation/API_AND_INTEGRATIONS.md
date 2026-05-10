# API And Integrations

Last updated: 2026-05-08

## FastAPI Layer

API files live under `api/`:

- `api/app.py`
- `api/main.py`
- `api/routes_models.py`
- `api/routes_results.py`
- `api/routes_scenarios.py`
- `api/routes_learning.py`
- `api/schemas.py`

## Current API Capabilities

- Health check.
- Demand prediction.
- County demand examples.
- Opportunity outputs.
- Segment outputs.
- Market access outputs.
- SML parse, validate, and run routes.
- Learning feedback, reports, lessons, apply, and rollback routes.

## External Integrations

### X/Twitter Trends

`x_trends.py` supports public aggregate trend fetching using `X_BEARER_TOKEN`.

### Hugging Face Spaces

The app deploys as a Gradio Space and syncs from GitHub Actions.

### GAMS

GAMS support is represented through code generation and runner helpers. GAMS is optional in local development and hosted deployment.

## Integration Principles

- Optional integrations must fail gracefully.
- Public UI should expose insights, not raw credentials or private records.
- Hosted environments should work with fallback data.

