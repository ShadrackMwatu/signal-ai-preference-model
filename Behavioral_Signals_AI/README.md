# Behavioral_Signals_AI

Behavioral_Signals_AI contains the behavioral intelligence side of Signal.

Canonical internal structure:

```text
adaptive_learning/
api/
app/
behavioral_ai/
dashboards/
explainability/
live_trends/
ml/
models/
training/
utils/
```

## Live Trend Intelligence

`live_trends/` contains the provider router for public aggregate trend feeds. It supports X aggregate trends, Google Trends compatible providers, optional third-party providers through environment variables, and a demo fallback when credentials are unavailable. See `Documentation/live_trend_intelligence.md`.