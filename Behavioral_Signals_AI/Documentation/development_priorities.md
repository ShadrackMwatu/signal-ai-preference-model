# Behavioral Signals AI Development Priorities

## Product Assessment

Behavioral Signals AI is a partially operational behavioral intelligence system. The public UI can run aggregate demand prediction and explanation today. The next development phase should consolidate the existing modules into a coherent AI-native behavioral engine.

## Roadmap

### Phase 1: Runtime Stabilization

Priority: immediate

- Normalize imports across live trends, app source modules, API modules, and training scripts.
- Add package initializers to active source folders.
- Keep Hugging Face startup green with no required external services.
- Add a route-level smoke test for the Behavioral Signals AI tab.
- Confirm root `app_routes/behavioral_route.py` and `Behavioral_Signals_AI/app/routes/behavioral_route.py` do not drift.

### Phase 2: Canonical Demand Intelligence Service

Priority: immediate

- Create a single demand prediction service that accepts aggregate features and returns classification, confidence, demand score, opportunity score, and source label.
- Route both Gradio and live trend intelligence through that service.
- Preserve fallback mode when model artifacts are missing.
- Document feature schema and model output schema.

### Phase 3: Behavioral Feature Engineering Upgrade

Priority: high

- Make `app/src/features/feature_engineering.py` canonical.
- Add schema validation for required raw columns.
- Add robust handling for missing/partial columns.
- Add county/category/time-period feature checks.
- Add feature drift summaries.

### Phase 4: Live Trend Intelligence

Priority: high

- Keep X/Twitter API optional.
- Normalize `privacy` imports.
- Add trend-cache outputs under ignored `Behavioral_Signals_AI/outputs/trend_cache/`.
- Convert trend records into the canonical demand service.
- Add location/county configuration beyond current demo locations.

### Phase 5: Opportunity Detection

Priority: high

- Expand `opportunity_engine.py` into a service with market gap, affordability, delivery, and competition dimensions.
- Link competitor analysis and market-access modules into one recommendation payload.
- Separate business recommendations from policy recommendations.

### Phase 6: Explainability

Priority: high

- Keep current rule-based explanation as the transparent baseline.
- Add model-aware explanations for trained models, such as permutation importance or feature contribution summaries.
- Add explanation confidence and caveat text.
- Ensure explanations never expose individual-level data.

### Phase 7: Adaptive Learning

Priority: medium

- Move feedback runtime storage to ignored Behavioral outputs.
- Record aggregate feedback events with model version, feature schema, prediction, observed label, and reviewer note.
- Add drift/retraining triggers.
- Require developer approval before replacing deployed model artifacts.

### Phase 8: Privacy-Preserving Analytics

Priority: medium

- Consolidate privacy filters into one canonical module.
- Enforce k-anonymity thresholds everywhere aggregate data is loaded.
- Add tests for blocked columns, PII-like text, small groups, and unsafe trend records.
- Document allowed data fields.

### Phase 9: AI-Native Forecasting

Priority: medium

- Add forecast service for county/category/time-period demand.
- Start with deterministic trend extrapolation and confidence intervals.
- Later add time-series models if data volume supports it.
- Keep all forecasts labeled as aggregate forecasts, not individual predictions.

### Phase 10: County-Level Intelligence

Priority: medium

- Use county as a first-class dimension in features, model outputs, and recommendations.
- Add county opportunity dashboards.
- Add county comparison tables and exportable summaries.
- Include county-level data sufficiency warnings.

### Phase 11: Business And Policy Recommendations

Priority: medium

- Convert opportunity outputs into structured recommendation types:
  - product/service opportunity
  - market access intervention
  - pricing/affordability issue
  - logistics or supply constraint
  - policy facilitation opportunity
- Add recommended next data collection actions.

## Immediate Next Modules To Build

1. `Behavioral_Signals_AI/app/src/services/demand_intelligence_service.py`
   - Central prediction service for Gradio, API, and trend intelligence.

2. `Behavioral_Signals_AI/app/src/services/behavioral_schema.py`
   - Required input/output schemas, validation, and defaults.

3. `Behavioral_Signals_AI/app/src/services/trend_signal_adapter.py`
   - Converts public aggregate trend records into canonical model features.

4. `Behavioral_Signals_AI/app/src/services/recommendation_service.py`
   - Combines opportunity, market access, competitor gaps, and explanation.

5. `Behavioral_Signals_AI/app/src/services/feedback_learning_service.py`
   - Records aggregate feedback and produces retraining recommendations.

6. `Behavioral_Signals_AI/tests/test_behavioral_runtime_imports.py`
   - Ensures canonical behavioral imports work without relying on legacy root paths.

## Definition Of Done For The Next Upgrade

- `app.py` still imports and launches.
- Behavioral route works without importing Signal_CGE internals.
- Live trend modules import directly without app-level fallback.
- Demand service returns the same visible fields as the current UI.
- Feedback writes only aggregate, privacy-safe records.
- Tests cover imports, prediction, explanation, privacy, trends, and fallback behavior.

