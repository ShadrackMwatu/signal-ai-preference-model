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
## Revealed Preference and Aggregate Demand Intelligence

Behavioral Signals AI is evolving into an AI-native behavioral-economic intelligence system. The backend now includes ingestion, analytics, revealed-preference inference, behavioral inference, demand intelligence, opportunity intelligence, recommendations, forecasting, and market intelligence layers. The public dashboard prioritizes decision-oriented Kenya-wide intelligence, while technical controls remain under Advanced Analytics.
## Multi-source Aggregate Signal Providers

`providers/` is the canonical provider layer for aggregate/public behavioral-economic signals. Phase 1 prioritizes search trends, X aggregate trends, optional news context, and demo fallback. Future provider namespaces cover social video, e-commerce, mobility, fintech, and app-store aggregates. All providers normalize to an aggregate public schema before entering revealed preference, demand intelligence, opportunity, recommendation, and forecasting engines.